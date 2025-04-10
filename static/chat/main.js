/**
 * 聊天页面主脚本
 */

// DOM元素
const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const clearConversationButton = document.getElementById('clear-conversation');
const renameConversationButton = document.getElementById('rename-conversation');
const deleteConversationButton = document.getElementById('delete-conversation');
const conversationTitle = document.getElementById('conversation-title');
const sidebarToggle = document.getElementById('sidebar-toggle');
const sidebar = document.querySelector('.sidebar');
const renameModal = document.getElementById('rename-modal');
const newTitleInput = document.getElementById('new-title');
const confirmRenameButton = document.getElementById('confirm-rename');
const cancelRenameButton = document.getElementById('cancel-rename');
const closeModal = document.querySelector('.close-modal');
const deleteConfirmDialog = document.getElementById('delete-confirm');
const confirmDeleteBtn = document.getElementById('confirm-delete');
const cancelDeleteBtn = document.getElementById('cancel-delete');
const floatingNewChatBtn = document.getElementById('floating-new-chat');

// 当前要删除的对话ID
let currentDeleteId = null;

// 侧边栏切换
if (sidebarToggle) {
    sidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
    });
}

// 发送消息事件处理
sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// 页面加载时聚焦到输入框
document.addEventListener('DOMContentLoaded', () => {
    messageInput.focus();

    // 检查系统暗色模式设置
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

    // 监听系统主题变化
    prefersDarkScheme.addEventListener('change', (e) => {
        console.log("系统主题变化:", e.matches ? "暗色模式" : "亮色模式");
    });
});

// 初始化时隐藏浮动按钮，仅在移动设备上显示
if (floatingNewChatBtn) {
    const updateFloatingButtonVisibility = () => {
        if (window.innerWidth <= 768) {
            floatingNewChatBtn.style.display = 'flex';
        } else {
            floatingNewChatBtn.style.display = 'none';
        }
    };

    // 初始检查
    updateFloatingButtonVisibility();

    // 监听窗口大小变化
    window.addEventListener('resize', updateFloatingButtonVisibility);
}

// 删除对话功能
if (deleteConversationButton) {
    deleteConversationButton.addEventListener('click', (e) => {
        currentDeleteId = conversationId;
        deleteConfirmDialog.style.display = 'flex';
    });
}

// 取消删除
if (cancelDeleteBtn) {
    cancelDeleteBtn.addEventListener('click', () => {
        deleteConfirmDialog.style.display = 'none';
        currentDeleteId = null;
    });
}

// 点击对话框外部关闭
if (deleteConfirmDialog) {
    deleteConfirmDialog.addEventListener('click', (e) => {
        if (e.target === deleteConfirmDialog) {
            deleteConfirmDialog.style.display = 'none';
            currentDeleteId = null;
        }
    });
}

// 确认删除
if (confirmDeleteBtn) {
    confirmDeleteBtn.addEventListener('click', async () => {
        if (!currentDeleteId) {
            deleteConfirmDialog.style.display = 'none';
            return;
        }

        try {
            // 显示删除中状态
            confirmDeleteBtn.disabled = true;
            confirmDeleteBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 删除中...';

            const response = await fetch(`/chat/${currentDeleteId}/delete/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                }
            });

            if (response.ok) {
                // 如果是当前对话，重定向到对话列表
                if (currentDeleteId === conversationId) {
                    window.location.href = '/chat/';
                } else {
                    // 否则从侧边栏中移除并关闭对话框
                    const item = document.querySelector(`.conversation-item[href="/chat/${currentDeleteId}/"]`);
                    if (item) {
                        item.remove();
                    }
                    deleteConfirmDialog.style.display = 'none';
                }
            } else {
                throw new Error('请求失败');
            }
        } catch (error) {
            console.error('删除对话出错:', error);
            alert('删除失败，请稍后重试');
            deleteConfirmDialog.style.display = 'none';
        } finally {
            // 重置按钮状态
            confirmDeleteBtn.disabled = false;
            confirmDeleteBtn.innerHTML = '确认删除';
            currentDeleteId = null;
        }
    });
}

// 清空对话内容
if (clearConversationButton) {
    clearConversationButton.addEventListener('click', () => {
        if (confirm('确定要清空这个对话的内容吗？此操作无法撤销。')) {
            // 清空前端显示
            chatMessages.innerHTML = `
                <div class="bot-message animate-fade-in">
                    <div class="avatar">E</div>
                    <div class="content">你好！我是Elepathy智能助手，很高兴为您服务。我可以回答问题、提供信息，或者聊聊天。请告诉我您需要什么帮助？</div>
                </div>
            `;

            // 清空服务器端对话内容
            fetch(`/chat/${conversationId}/clear/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                }
            }).catch(error => {
                console.error('清空对话内容失败:', error);
            });
        }
    });
}

// 重命名对话
if (renameConversationButton) {
    renameConversationButton.addEventListener('click', () => {
        newTitleInput.value = conversationTitle.textContent.replace(' (由DeepSeek驱动)', '').trim();
        renameModal.style.display = 'flex';
        newTitleInput.focus();
        newTitleInput.select();
    });
}

// 确认重命名
if (confirmRenameButton) {
    confirmRenameButton.addEventListener('click', renameConversation);
}

// 取消重命名
if (cancelRenameButton) {
    cancelRenameButton.addEventListener('click', () => {
        renameModal.style.display = 'none';
    });
}

// 点击关闭按钮
if (closeModal) {
    closeModal.addEventListener('click', () => {
        renameModal.style.display = 'none';
    });
}

// 点击模态框外部关闭
window.addEventListener('click', (e) => {
    if (e.target === renameModal) {
        renameModal.style.display = 'none';
    }
});

// 删除对话按钮事件
document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
        e.preventDefault();
        e.stopPropagation();
        const id = e.target.closest('.delete-btn').dataset.id;
        currentDeleteId = id;
        deleteConfirmDialog.style.display = 'flex';
    });
});

// 重命名对话按钮事件（列表中的）
document.querySelectorAll('.rename-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const id = e.target.closest('.rename-btn').dataset.id;
        const title = e.target.closest('.conversation-item').querySelector('.conversation-title').textContent.trim();

        // 如果点击的是当前对话，使用页面上的重命名按钮
        if (id === conversationId) {
            renameConversationButton.click();
        } else {
            // 否则显示重命名模态框，设置ID和标题
            newTitleInput.value = title;
            newTitleInput.dataset.id = id;
            renameModal.style.display = 'flex';
            newTitleInput.focus();
            newTitleInput.select();
        }
    });
});

/**
 * 删除对话
 * @param {string} id - 对话ID
 */
async function deleteConversation(id) {
    currentDeleteId = id;
    deleteConfirmDialog.style.display = 'flex';
}

/**
 * 重命名对话
 */
async function renameConversation() {
    const newTitle = newTitleInput.value.trim();

    if (!newTitle) {
        alert('标题不能为空');
        return;
    }

    // 获取对话ID - 如果是侧边栏触发的，使用input的data-id属性
    const id = newTitleInput.dataset.id || conversationId;

    try {
        const response = await fetch(`/chat/${id}/rename/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({ title: newTitle })
        });

        if (response.ok) {
            // 关闭模态框
            renameModal.style.display = 'none';

            // 如果是当前对话，更新标题
            if (id === conversationId) {
                conversationTitle.innerHTML = `${newTitle} <small>(由DeepSeek驱动)</small>`;
            }

            // 更新侧边栏中的标题
            const sidebarItem = document.querySelector(`.conversation-item[href="/chat/${id}/"] .conversation-title`);
            if (sidebarItem) {
                sidebarItem.textContent = newTitle;
            }

            // 清除临时数据
            newTitleInput.dataset.id = '';
        } else {
            alert('重命名失败，请稍后重试');
        }
    } catch (error) {
        console.error('重命名对话出错:', error);
        alert('发生错误，请稍后重试');
    }
}

/**
 * 发送消息并处理响应
 */
function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    // 添加用户消息到聊天
    addUserMessage(message);
    messageInput.value = '';

    // 显示"正在输入"指示器
    const typingMessageId = addTypingIndicator();

    // 禁用发送按钮，表示等待中
    toggleSendButton(false);

    // 调用聊天API
    fetch(`/chat/${conversationId}/api/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({ message: message }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('网络错误，请稍后再试');
            }
            return response.json();
        })
        .then(data => {
            // 移除"正在输入"指示器
            removeTypingIndicator(typingMessageId);

            // 显示机器人回复
            if (data.status === 'success') {
                addBotMessage(data.message);

                // 如果返回了新标题，更新页面标题
                if (data.title && data.title !== conversationTitle.textContent.replace(' (由DeepSeek驱动)', '').trim()) {
                    conversationTitle.innerHTML = `${data.title} <small>(由DeepSeek驱动)</small>`;

                    // 更新侧边栏中的标题
                    const sidebarItem = document.querySelector(`.conversation-item[href="/chat/${conversationId}/"] .conversation-title`);
                    if (sidebarItem) {
                        sidebarItem.textContent = data.title;
                    }
                }
            } else {
                addBotMessage('抱歉，处理您的请求时出现了问题：' + data.message);
            }
        })
        .catch(error => {
            // 移除"正在输入"指示器
            removeTypingIndicator(typingMessageId);

            // 显示错误消息
            addBotMessage(`发生错误: ${error.message}`);
        })
        .finally(() => {
            // 恢复发送按钮
            toggleSendButton(true);
            // 聚焦输入框
            messageInput.focus();
        });
}

/**
 * 获取CSRF Token
 */
function getCsrfToken() {
    // 从cookie获取CSRF token
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];

    return cookieValue || '';
}

/**
 * 添加用户消息到聊天窗口
 * @param {string} message - 用户消息文本
 */
function addUserMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.className = 'user-message animate-fade-in';

    // 处理消息文本，支持简单的URL识别和换行
    const messageText = formatMessageText(message);

    messageElement.innerHTML = `
        <div class="avatar">U</div>
        <div class="content">${messageText}</div>
    `;

    chatMessages.appendChild(messageElement);
    scrollToBottom();
}

/**
 * 添加机器人消息到聊天窗口
 * @param {string} message - 机器人消息文本
 * @param {boolean} isFirstMessage - 是否是欢迎消息
 */
function addBotMessage(message, isFirstMessage = false) {
    const messageElement = document.createElement('div');
    messageElement.className = `bot-message animate-fade-in ${isFirstMessage ? 'first-message' : ''}`;

    // 处理消息文本，支持简单的URL识别和换行
    const messageText = formatMessageText(message);

    messageElement.innerHTML = `
        <div class="avatar">E</div>
        <div class="content">${messageText}</div>
    `;

    chatMessages.appendChild(messageElement);
    scrollToBottom();
}

/**
 * 添加"正在输入"指示器
 * @returns {string} 指示器元素的唯一ID
 */
function addTypingIndicator() {
    const id = 'typing-' + Date.now();
    const messageElement = document.createElement('div');
    messageElement.className = 'bot-message';
    messageElement.id = id;

    messageElement.innerHTML = `
        <div class="avatar">E</div>
        <div class="content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;

    chatMessages.appendChild(messageElement);
    scrollToBottom();
    return id;
}

/**
 * 移除"正在输入"指示器
 * @param {string} id - 指示器元素的唯一ID
 */
function removeTypingIndicator(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}

/**
 * 格式化消息文本，支持URL识别和换行
 * @param {string} text - 原始消息文本
 * @returns {string} 格式化后的HTML
 */
function formatMessageText(text) {
    // 转义HTML字符
    let formattedText = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

    // 简单的URL识别
    formattedText = formattedText.replace(
        /(https?:\/\/[^\s]+)/g,
        '<a href="$1" target="_blank" class="text-primary underline">$1</a>'
    );

    // 处理换行
    formattedText = formattedText.replace(/\n/g, '<br>');

    return formattedText;
}

/**
 * 切换发送按钮的启用/禁用状态
 * @param {boolean} enabled - 是否启用按钮
 */
function toggleSendButton(enabled) {
    sendButton.disabled = !enabled;
    sendButton.innerHTML = enabled
        ? '<i class="fas fa-paper-plane"></i> 发送'
        : '<i class="fas fa-spinner fa-spin"></i> 发送中';
}

/**
 * 滚动到聊天窗口底部
 */
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
