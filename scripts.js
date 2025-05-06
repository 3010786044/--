// 确保 particles.js 在 DOM 加载完成后初始化，避免找不到元素
document.addEventListener('DOMContentLoaded', function() {
    particlesJS('particles-js', {
        "particles": {
            "number": {
                "value": 80,
                "density": {
                    "enable": true,
                    "value_area": 800
                }
            },
            "color": {
                "value": "#66FCF1" // 设置粒子颜色为炫酷的颜色
            },
            "shape": {
                "type": "circle",
                "stroke": {
                    "width": 0,
                    "color": "#000000"
                },
                "polygon": {
                    "nb_sides": 5
                }
            },
            "opacity": {
                "value": 0.5,
                "random": false,
                "anim": {
                    "enable": false,
                    "speed": 1,
                    "opacity_min": 0.1,
                    "sync": false
                }
            },
            "size": {
                "value": 4,
                "random": true,
                "anim": {
                    "enable": false,
                    "speed": 40,
                    "size_min": 0.1,
                    "sync": false
                }
            },
            "line_linked": {
                "enable": true,
                "distance": 150,
                "color": "#66FCF1",
                "opacity": 0.4,
                "width": 1
            },
            "move": {
                "enable": true,
                "speed": 6,
                "direction": "none",
                "random": false,
                "straight": false,
                "out_mode": "out",
                "bounce": false,
                "attract": {
                    "enable": false,
                    "rotateX": 600,
                    "rotateY": 1200
                }
            }
        },
        "interactivity": {
            "detect_on": "canvas",
            "events": {
                "onhover": {
                    "enable": true,
                    "mode": "repulse"
                },
                "onclick": {
                    "enable": true,
                    "mode": "push"
                },
                "resize": true
            },
            "modes": {
                "grab": {
                    "distance": 400,
                    "line_linked": {
                        "opacity": 1
                    }
                },
                "bubble": {
                    "distance": 400,
                    "size": 40,
                    "duration": 2,
                    "opacity": 8,
                    "speed": 3
                },
                "repulse": {
                    "distance": 200,
                    "duration": 0.4
                },
                "push": {
                    "particles_nb": 4
                },
                "remove": {
                    "particles_nb": 2
                }
            }
        },
        "retina_detect": true
    });

    // 添加搜索按钮点击事件
    const searchButton = document.getElementById('searchButton');
    if (searchButton) {
        searchButton.addEventListener('click', performSearch);
    }
    
    // 添加回车键搜索功能
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
});

// 加载模态框
window.onload = function() {
    loadComments(); // 加载评论
    document.getElementById('welcomeModal').style.display = 'block'; // 显示模态框

    // 为开始搜索按钮添加点击事件
    document.getElementById('focusSearchButton').onclick = function() {
        closeModal(); // 关闭模态框
        document.getElementById('searchInput').focus(); // 将焦点设置到搜索框
    };
};

// 关闭模态框函数
function closeModal() {
    document.getElementById('welcomeModal').style.display = 'none'; // 隐藏模态框
}

// 当用户点击模态框外部，关闭模态框
window.onclick = function(event) {
    let modal = document.getElementById('welcomeModal');
    if (event.target === modal) {
        closeModal(); // 隐藏模态框
    }
};

// 提交评论函数
const deletePassword = "520"; // 设置删除评论的密码

function submitComment() {
    let commentInput = document.getElementById('commentInput');
    let commentText = commentInput.value.trim();
    if (commentText) {
        let comments = getCommentsFromLocalStorage(); // 获取现有评论
        let timestamp = new Date().toLocaleString(); // 获取当前时间
        comments.push({ text: commentText, time: timestamp }); // 添加新评论和时间戳
        localStorage.setItem('comments', JSON.stringify(comments)); // 保存评论到本地存储
        commentInput.value = ''; // 清空输入框
        loadComments(); // 重新加载评论
    } else {
        alert("评论不能为空！");
    }
}

// 从本地存储获取评论
function getCommentsFromLocalStorage() {
    let comments = localStorage.getItem('comments');
    return comments ? JSON.parse(comments) : []; // 返回已存储的评论或空数组
}

// 加载评论并显示
function loadComments() {
    let commentsDiv = document.getElementById('comments');
    commentsDiv.innerHTML = ''; // 清空当前评论显示区域
    let comments = getCommentsFromLocalStorage(); // 获取评论
    comments.forEach((comment, index) => {
        let newComment = document.createElement('div');
        newComment.textContent = `${comment.text} (发表于: ${comment.time})`; // 显示评论和时间戳
        
        // 创建删除按钮
        let deleteButton = document.createElement('button');
        deleteButton.textContent = '删除';
        deleteButton.onclick = function() {
            let password = prompt("请输入删除评论的密码："); // 输入密码
            if (password === deletePassword) {
                deleteComment(index); // 如果密码正确，删除评论
            } else {
                alert("密码错误！");
            }
        };
        
        newComment.appendChild(deleteButton); // 将删除按钮添加到评论
        newComment.style.backgroundColor = "#1F2833";
        newComment.style.padding = "10px";
        newComment.style.margin = "5px 0";
        newComment.style.borderRadius = "5px";
        commentsDiv.appendChild(newComment);
    });
}

// 删除评论函数
function deleteComment(index) {
    let comments = getCommentsFromLocalStorage(); // 获取现有评论
    comments.splice(index, 1); // 删除指定索引的评论
    localStorage.setItem('comments', JSON.stringify(comments)); // 更新本地存储
    loadComments(); // 重新加载评论
}

// 修改链接点击处理代码
document.querySelectorAll('.resource-list li').forEach(item => {
    item.addEventListener('click', () => {
        const link = item.querySelector('a');
        if (link) {
            // 在新窗口打开链接
            window.open(link.href, '_blank'); // 修改这里，使用 window.open
            return false; // 阻止默认行为
        }
    });
});

// 修改搜索功能，也在新窗口打开
function performSearch() {
    const searchInput = document.getElementById('searchInput').value;
    if (searchInput.trim() !== '') {
        // 使用百度接口进行搜索，在新窗口打开
        window.open('https://www.baidu.com/s?wd=' + encodeURIComponent(searchInput), '_blank');
    }
}

// 确保页面加载时始终从顶部开始显示
window.onbeforeunload = function () {
    window.scrollTo(0, 0);
};