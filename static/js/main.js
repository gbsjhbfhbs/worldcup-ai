/**
 * 通用前端交互
 */

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', () => {
    // 高亮当前导航链接
    highlightCurrentNav();
});

function highlightCurrentNav() {
    const path = window.location.pathname;
    document.querySelectorAll('.nav-links a').forEach(a => {
        const href = a.getAttribute('href');
        if (href === '/' && path === '/') {
            a.style.color = 'var(--text)';
        } else if (href !== '/' && path.startsWith(href)) {
            a.style.color = 'var(--text)';
        }
    });
}
