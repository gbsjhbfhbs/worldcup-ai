"""AI API 封装 — 直接 HTTP 调用（绕过 SDK SSL 兼容问题）"""
import json
import ssl
import time
import urllib.request

from config import Config


class AIClientError(Exception):
    """AI 服务调用错误"""
    pass


class AIClient:
    """Anthropic 兼容 API 客户端（urllib 直连，跳过 SSL 校验）"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.ANTHROPIC_API_KEY
        if not self.api_key:
            raise AIClientError(
                "未设置 API Key。请在环境变量中设置 ANTHROPIC_API_KEY 或 ANTHROPIC_AUTH_TOKEN"
            )
        self.base_url = (Config.ANTHROPIC_BASE_URL or "https://api.anthropic.com").rstrip("/")

    def call(self, system_prompt: str, user_prompt: str,
             model: str = None, max_tokens: int = 2000) -> str:
        """同步调用 AI API，含重试和错误处理"""
        model = model or Config.PREDICTION_MODEL
        url = f"{self.base_url}/messages"

        # 构造请求体
        messages = [{"role": "user", "content": user_prompt}]
        body = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages,
        }
        if system_prompt:
            body["system"] = system_prompt

        # 构造 SSL 上下文（跳过证书校验，适配企业代理环境）
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        last_error = None
        for attempt in range(Config.MAX_RETRIES + 1):
            try:
                data = json.dumps(body).encode("utf-8")
                req = urllib.request.Request(url, data=data, headers=headers, method="POST")
                resp = urllib.request.urlopen(req, context=ctx, timeout=Config.REQUEST_TIMEOUT)

                result = json.loads(resp.read().decode("utf-8"))

                # 解析 Anthropic 格式响应
                if "content" in result:
                    content = result["content"]
                    if isinstance(content, list):
                        texts = []
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "text":
                                texts.append(block["text"])
                        return "\n".join(texts)
                    elif isinstance(content, str):
                        return content
                # 兼容 OpenAI 格式
                if "choices" in result:
                    return result["choices"][0]["message"]["content"]

                return str(result)

            except urllib.error.HTTPError as e:
                status = e.code
                error_body = ""
                try:
                    error_body = e.read().decode("utf-8")[:500]
                except Exception:
                    pass

                if status == 429:
                    wait = 2 ** attempt
                    print(f"[AIClient] 速率限制，{wait}s 后重试 ({attempt + 1}/{Config.MAX_RETRIES})")
                    time.sleep(wait)
                    last_error = e
                elif status >= 500:
                    wait = 2 ** attempt
                    print(f"[AIClient] 服务端错误 {status}，{wait}s 后重试")
                    time.sleep(wait)
                    last_error = e
                else:
                    raise AIClientError(f"API 错误 ({status}): {error_body}")

            except (IOError, OSError, Exception) as e:
                error_str = str(e)
                if "timed out" in error_str.lower() or "timeout" in error_str.lower():
                    print(f"[AIClient] 超时，重试 ({attempt + 1}/{Config.MAX_RETRIES})")
                    last_error = e
                    time.sleep(2)
                else:
                    print(f"[AIClient] 连接错误: {error_str[:100]}")
                    if attempt < Config.MAX_RETRIES:
                        time.sleep(2 ** attempt)
                    last_error = e

        raise AIClientError(
            f"API 调用失败，已重试 {Config.MAX_RETRIES} 次。最后错误: {last_error}"
        )
