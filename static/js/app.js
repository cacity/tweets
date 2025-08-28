/**
 * Twitter RSS订阅管理器 - 通用JavaScript功能
 */

// 全局变量
window.toastContainer = null;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeToastContainer();
    initializeTooltips();
    initializeAnimations();
});

/**
 * 初始化Toast容器
 */
function initializeToastContainer() {
    if (!window.toastContainer) {
        window.toastContainer = document.createElement('div');
        window.toastContainer.className = 'toast-container';
        document.body.appendChild(window.toastContainer);
    }
}

/**
 * 显示Toast消息
 */
function showToast(message, type = 'info', duration = 5000) {
    const toastId = 'toast-' + Date.now();
    const iconMap = {
        'success': 'bi-check-circle-fill',
        'error': 'bi-x-circle-fill',
        'warning': 'bi-exclamation-triangle-fill',
        'info': 'bi-info-circle-fill'
    };
    
    const colorMap = {
        'success': 'text-success',
        'error': 'text-danger',
        'warning': 'text-warning',
        'info': 'text-primary'
    };
    
    const toastHtml = `
        <div class="toast align-items-center border-0" id="${toastId}" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body d-flex align-items-center">
                    <i class="bi ${iconMap[type]} ${colorMap[type]} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    window.toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        delay: duration
    });
    
    toast.show();
    
    // 自动移除DOM元素
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

/**
 * 初始化工具提示
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * 初始化动画效果
 */
function initializeAnimations() {
    // 为卡片添加渐入动画
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in-up');
    });
    
    // 监听滚动事件，添加视差效果
    window.addEventListener('scroll', handleScroll);
}

/**
 * 滚动事件处理
 */
function handleScroll() {
    const scrolled = window.pageYOffset;
    const parallax = document.querySelector('.parallax');
    
    if (parallax) {
        const speed = 0.5;
        parallax.style.transform = `translateY(${scrolled * speed}px)`;
    }
}

/**
 * 确认对话框
 */
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

/**
 * 复制文本到剪贴板
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('已复制到剪贴板', 'success');
        return true;
    } catch (err) {
        console.error('复制失败:', err);
        showToast('复制失败', 'error');
        return false;
    }
}

/**
 * 格式化文件大小
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * 格式化日期
 */
function formatDate(dateString, options = {}) {
    const date = new Date(dateString);
    const defaultOptions = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    
    return date.toLocaleDateString('zh-CN', { ...defaultOptions, ...options });
}

/**
 * 防抖函数
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * 节流函数
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * 检查URL有效性
 */
function isValidUrl(url) {
    try {
        new URL(url);
        return true;
    } catch (e) {
        return false;
    }
}

/**
 * 安全的HTML转义
 */
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

/**
 * 加载状态管理
 */
class LoadingManager {
    constructor() {
        this.loadingStates = new Set();
    }
    
    show(id, element, text = '加载中...') {
        if (this.loadingStates.has(id)) return;
        
        this.loadingStates.add(id);
        
        if (element) {
            element.dataset.originalText = element.innerHTML;
            element.innerHTML = `<i class="bi bi-arrow-clockwise spin me-1"></i>${text}`;
            element.disabled = true;
        }
    }
    
    hide(id, element) {
        if (!this.loadingStates.has(id)) return;
        
        this.loadingStates.delete(id);
        
        if (element && element.dataset.originalText) {
            element.innerHTML = element.dataset.originalText;
            element.disabled = false;
            delete element.dataset.originalText;
        }
    }
}

// 全局加载管理器实例
window.loadingManager = new LoadingManager();

/**
 * API请求封装
 */
class ApiClient {
    static async request(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
            ...options
        };
        
        try {
            const response = await fetch(url, defaultOptions);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || `HTTP error! status: ${response.status}`);
            }
            
            return data;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }
    
    static async get(url) {
        return this.request(url, { method: 'GET' });
    }
    
    static async post(url, data) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    static async delete(url) {
        return this.request(url, { method: 'DELETE' });
    }
}

// 全局API客户端
window.api = ApiClient;

/**
 * 全局错误处理
 */
window.addEventListener('error', function(e) {
    console.error('全局错误:', e.error);
    showToast('发生了未知错误，请刷新页面重试', 'error');
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('未处理的Promise拒绝:', e.reason);
    showToast('网络请求失败，请检查网络连接', 'error');
});

/**
 * 页面可见性变化处理
 */
document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        // 页面变为可见时，可以执行一些刷新操作
        console.log('页面变为可见');
    }
});

// 添加CSS动画样式
const style = document.createElement('style');
style.textContent = `
.spin {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.fade-in-up {
    animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
}

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #1da1f2;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}
`;
document.head.appendChild(style);