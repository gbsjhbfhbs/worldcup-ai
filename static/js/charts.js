/**
 * Canvas 图表库 — 雷达图、柱状图
 * 零依赖，纯 Canvas API 实现
 */

// ============================================================
// 雷达图（球队能力对比）
// ============================================================
function drawRadarChart(canvasId, labels, data1, data2, label1, label2) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const W = canvas.width = canvas.parentElement.clientWidth - 32;
    const H = canvas.height = Math.min(W * 0.7, 350);

    const cx = W / 2, cy = H / 2;
    const radius = Math.min(cx, cy) - 40;
    const sides = labels.length;
    const angleStep = (Math.PI * 2) / sides;

    // 背景网格
    for (let r = 1; r <= 5; r++) {
        ctx.beginPath();
        for (let i = 0; i < sides; i++) {
            const a = -Math.PI / 2 + angleStep * i;
            const x = cx + radius * (r / 5) * Math.cos(a);
            const y = cy + radius * (r / 5) * Math.sin(a);
            i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.strokeStyle = 'rgba(255,255,255,0.08)';
        ctx.stroke();
    }

    // 轴线
    for (let i = 0; i < sides; i++) {
        const a = -Math.PI / 2 + angleStep * i;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(cx + radius * Math.cos(a), cy + radius * Math.sin(a));
        ctx.strokeStyle = 'rgba(255,255,255,0.1)';
        ctx.stroke();

        // 标签
        const lx = cx + (radius + 20) * Math.cos(a);
        const ly = cy + (radius + 20) * Math.sin(a);
        ctx.fillStyle = '#8888aa';
        ctx.font = '12px "Microsoft YaHei", sans-serif';
        ctx.textAlign = a > Math.PI * 0.5 || a < -Math.PI * 0.5 ? 'right' : a === Math.PI * 0.5 || a === -Math.PI * 0.5 ? 'center' : 'left';
        ctx.textBaseline = a > 0 && a < Math.PI ? 'top' : 'bottom';
        ctx.fillText(labels[i], lx, ly);
    }

    // 绘制数据
    drawRadarLayer(ctx, cx, cy, radius, sides, angleStep, data1, 'rgba(0, 212, 170, 0.6)', 'rgba(0, 212, 170, 0.2)');
    drawRadarLayer(ctx, cx, cy, radius, sides, angleStep, data2, 'rgba(255, 107, 107, 0.6)', 'rgba(255, 107, 107, 0.2)');

    // 图例
    ctx.font = '12px "Microsoft YaHei", sans-serif';
    const lx = 12, ly = 22;
    ctx.fillStyle = 'rgba(0, 212, 170, 0.8)';
    ctx.fillRect(lx, ly - 8, 12, 12);
    ctx.fillStyle = '#e0e0e0';
    ctx.textAlign = 'left';
    ctx.fillText(label1, lx + 18, ly + 2);

    ctx.fillStyle = 'rgba(255, 107, 107, 0.8)';
    ctx.fillRect(lx + 100, ly - 8, 12, 12);
    ctx.fillText(label2, lx + 118, ly + 2);
}

function drawRadarLayer(ctx, cx, cy, radius, sides, angleStep, data, strokeColor, fillColor) {
    ctx.beginPath();
    for (let i = 0; i < sides; i++) {
        const a = -Math.PI / 2 + angleStep * i;
        const v = Math.max(0.05, Math.min(1, data[i]));
        const x = cx + radius * v * Math.cos(a);
        const y = cy + radius * v * Math.sin(a);
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.fillStyle = fillColor;
    ctx.fill();
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = 2;
    ctx.stroke();

    // 数据点
    for (let i = 0; i < sides; i++) {
        const a = -Math.PI / 2 + angleStep * i;
        const v = Math.max(0.05, Math.min(1, data[i]));
        ctx.beginPath();
        ctx.arc(cx + radius * v * Math.cos(a), cy + radius * v * Math.sin(a), 4, 0, Math.PI * 2);
        ctx.fillStyle = strokeColor;
        ctx.fill();
    }
}


// ============================================================
// 柱状图（夺冠概率/胜率）
// ============================================================
function drawBarChart(canvasId, labels, values, colors) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const W = canvas.width = Math.max(canvas.parentElement.clientWidth - 32, 400);
    const H = canvas.height = Math.max(labels.length * 32 + 40, 200);

    const padLeft = 100, padRight = 50, padTop = 10, padBottom = 20;
    const chartW = W - padLeft - padRight;
    const chartH = H - padTop - padBottom;
    const barH = Math.min(chartH / labels.length - 4, 28);
    const maxVal = Math.max(...values, 0.01);

    ctx.clearRect(0, 0, W, H);

    values.forEach((v, i) => {
        const y = padTop + i * (chartH / labels.length);
        const bw = Math.max(2, (v / maxVal) * chartW);

        // 标签
        ctx.fillStyle = '#e0e0e0';
        ctx.font = '12px "Microsoft YaHei", sans-serif';
        ctx.textAlign = 'right';
        ctx.fillText(labels[i], padLeft - 8, y + barH / 2 + 4);

        // 背景
        ctx.fillStyle = 'rgba(255,255,255,0.03)';
        ctx.fillRect(padLeft, y, chartW, barH);

        // 柱体
        const color = colors?.[i] || 'rgba(0, 212, 170, 0.8)';
        ctx.fillStyle = color;
        ctx.fillRect(padLeft, y + 2, bw, barH - 4);

        // 数值
        ctx.fillStyle = '#ffd700';
        ctx.textAlign = 'left';
        ctx.fillText((values[i] * 100).toFixed(1) + '%', padLeft + bw + 6, y + barH / 2 + 4);
    });
}


// ============================================================
// 骨架屏
// ============================================================
function showSkeleton(containerId, type) {
    const el = document.getElementById(containerId);
    if (!el) return;
    if (type === 'card') {
        el.innerHTML = `
            <div class="skeleton-card">
                <div class="skeleton-line w-60"></div>
                <div class="skeleton-line w-80"></div>
                <div class="skeleton-line w-40"></div>
            </div>`;
    } else if (type === 'bars') {
        el.innerHTML = Array(5).fill(`
            <div class="skeleton-bar">
                <div class="skeleton-line w-30"></div>
                <div class="skeleton-track"><div class="skeleton-fill"></div></div>
            </div>`).join('');
    } else if (type === 'text') {
        el.innerHTML = Array(4).fill('<div class="skeleton-line w-full"></div>').join('');
    }
}


// ============================================================
// 预测准确率计算
// ============================================================
function calcBrierScore(predictions) {
    // Brier Score = 1/N * sum((pred - actual)^2)
    // predictions: [{home_win_prob, draw_prob, away_win_prob, actual_outcome: 'H'|'D'|'A'}]
    if (!predictions.length) return null;
    let score = 0;
    predictions.forEach(p => {
        const actual = { H: [1, 0, 0], D: [0, 1, 0], A: [0, 0, 1] }[p.actual_outcome];
        const pred = [p.home_win_prob, p.draw_prob, p.away_win_prob];
        score += (pred[0] - actual[0]) ** 2 + (pred[1] - actual[1]) ** 2 + (pred[2] - actual[2]) ** 2;
    });
    return score / predictions.length;
}
