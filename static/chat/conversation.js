// 当前要删除的对话ID
let currentDeleteId = null;
const deleteConfirmDialog = document.getElementById('delete-confirm');
const confirmDeleteBtn = document.getElementById('confirm-delete');
const cancelDeleteBtn = document.getElementById('cancel-delete');

// 删除对话功能 - 显示确认对话框
document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();

        const id = e.target.closest('.delete-btn').dataset.id;
        currentDeleteId = id;

        // 显示确认对话框
        deleteConfirmDialog.style.display = 'flex';
    });
});

// 取消删除
cancelDeleteBtn.addEventListener('click', () => {
    deleteConfirmDialog.style.display = 'none';
    currentDeleteId = null;
});

// 点击对话框外部关闭
deleteConfirmDialog.addEventListener('click', (e) => {
    if (e.target === deleteConfirmDialog) {
        deleteConfirmDialog.style.display = 'none';
        currentDeleteId = null;
    }
});

// 确认删除
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
            // 删除成功，关闭对话框
            deleteConfirmDialog.style.display = 'none';

            // 添加删除动画
            const card = document.querySelector(`.conversation-card[data-id="${currentDeleteId}"]`);
            if (card) {
                card.style.transform = 'translateX(100%)';
                card.style.opacity = '0';

                // 动画结束后移除元素
                setTimeout(() => {
                    card.remove();

                    // 如果全部删除了，显示空状态
                    if (document.querySelectorAll('.conversation-card').length === 0) {
                        location.reload();
                    }
                }, 300);
            }
        } else {
            throw new Error('请求失败');
        }
    } catch (error) {
        console.error('删除对话出错:', error);
        alert('删除失败，请稍后重试');
    } finally {
        // 重置按钮状态
        confirmDeleteBtn.disabled = false;
        confirmDeleteBtn.innerHTML = '确认删除';
        currentDeleteId = null;
    }
});

/**
 * 获取CSRF Token
 */
function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];

    return cookieValue || '';
}
