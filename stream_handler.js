// 流式报告生成器
function handleStreamReport() {
    const year = document.getElementById('year').value;
    const month = document.getElementById('month').value;
    const day = document.getElementById('day').value;
    
    if (!year || !month || !day) {
        alert('请选择完整的日期');
        return;
    }
    
    // 显示 Loading 动画
    document.getElementById('loadingOverlay').classList.add('active');
    document.getElementById('submitBtn').disabled = true;
    
    // 启动粒子效果
    startParticles();
    
    // 启动文字轮播
    startTextRotation();
    
    // 创建 FormData 对象
    const formData = new FormData();
    formData.append('year', year);
    formData.append('month', month);
    formData.append('day', day);
    
    // 进度条和文字
    let progressStep = 0;
    const progressTexts = [
        '商业潜能计算中...',
        '能量场解析中...',
        'AI 算法推演中...',
        '商业蓝图生成中...',
        '个性化报告组装中...'
    ];
    
    function updateProgress(percent, text) {
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        
        if (progressBar) {
            progressBar.style.width = `${percent * 100}%`;
        }
        
        if (progressText) {
            progressText.textContent = text;
        }
    }
    
    function finishReport(fullContent) {
        console.log('报告生成完成');
        
        // 停止粒子效果
        stopParticles();
        
        // 停止文字轮播
        stopTextRotation();
        
        // 隐藏 Loading 动画
        document.getElementById('loadingOverlay').classList.remove('active');
        document.getElementById('submitBtn').disabled = false;
        
        // 隐藏表单容器
        document.querySelector('.container').style.display = 'none';
        
        // 创建结果容器
        const resultContainer = document.createElement('div');
        resultContainer.className = 'result-container';
        resultContainer.id = 'result';
        
        // 使用marked解析Markdown
        resultContainer.innerHTML = marked.parse(fullContent);
        
        // 提取主图腾名称
        const kinMatch = fullContent.match(/主图腾：([^\s]+)\s*[-–—]/);
        const kinName = kinMatch ? kinMatch[1] : '';
        const greeting = kinName ? `亲爱的${kinName}印记持有者` : '亲爱的创业者';
        
        // 添加金句展示（社交货币属性）
        const goldenQuotes = {
            '红龙': '红龙：在废墟中重生，在黎明前觉醒',
            '白风': '白风：用呼吸创造奇迹，用语言改变世界',
            '蓝夜': '蓝夜：在黑暗中看见光，在寂静中听见真理',
            '黄种子': '黄种子：不在低谷退场，只在顶峰相见',
            '红蛇': '红蛇：用直觉穿透迷雾，用行动定义未来',
            '白世界桥': '白世界桥：跨越生死界限，连接无限可能',
            '蓝手': '蓝手：用双手雕刻梦想，用匠心铸就传奇',
            '黄星星': '黄星星：在平凡中发现美，在黑暗中点亮光',
            '红月': '红月：用情感滋养生命，用直觉指引方向',
            '白狗': '白狗：用真心换取信任，用忠诚赢得永恒',
            '蓝猴': '蓝猴：在游戏中寻找真理，在欢笑中释放灵魂',
            '黄人': '黄人：用智慧点亮人生，用选择定义命运',
            '红天行者': '红天行者：跨越时空边界，探索无限可能',
            '巫师': '巫师：用魔法改变现实，用直觉洞察未来',
            '蓝鹰': '蓝鹰：从高空俯瞰世界，用视野创造奇迹',
            '黄战士': '黄战士：在挑战中成长，在战斗中觉醒',
            '红地球': '红地球：脚踏实地前行，用行动改变世界',
            '白镜子': '白镜子：在反射中发现真相，在镜像中看见自己',
            '蓝风暴': '蓝风暴：在变革中寻找机遇，在风暴中创造新生',
            '太阳': '太阳：用光芒照亮世界，用温暖治愈心灵',
            '红龙': '红龙：在废墟中重生，在黎明前觉醒',
            '白风': '白风：用呼吸创造奇迹，用语言改变世界',
            '蓝夜': '蓝夜：在黑暗中看见光，在寂静中听见真理',
            '黄种子': '黄种子：不在低谷退场，只在顶峰相见'
        };
        
        const goldenQuote = goldenQuotes[kinName] || `${kinName}：用天赋创造财富，用行动定义人生`;
        
        const quoteCard = document.createElement('div');
        quoteCard.className = 'quote-card';
        quoteCard.style.cssText = `
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.2) 0%, rgba(10, 10, 10, 0.9) 100%);
            border: 2px solid #D4AF37;
            border-radius: 16px;
            padding: 24px;
            margin: 20px auto;
            max-width: 600px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(212, 175, 55, 0.3);
            backdrop-filter: blur(10px);
        `;
        quoteCard.innerHTML = `
            <h2 style="color: #D4AF37; margin-bottom: 15px; font-size: 1.5em;">${greeting}</h2>
            <p style="color: #E5E7EB; font-size: 1.3em; line-height: 1.8; margin: 0; font-style: italic;">"${goldenQuote}"</p>
            <button onclick="shareToSocial()" style="margin-top: 20px; padding: 12px 24px; background: linear-gradient(135deg, #D4AF37 0%, #A67C00 100%); border: none; border-radius: 8px; color: #1A1A1A; font-size: 1em; font-weight: bold; cursor: pointer; transition: all 0.3s ease;">📸 生成分享海报</button>
        `;
        
        // 插入金句卡片
        const firstElement = resultContainer.firstChild;
        resultContainer.insertBefore(quoteCard, firstElement);
        
        // 插入到页面
        document.body.appendChild(resultContainer);
        
        // 平滑滚动到结果
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    // 发送请求（使用流式传输）
    fetch('/stream_report', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('网络响应异常');
        }
        
        // 处理流式响应
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullContent = '';
        
        function readStream() {
            return reader.read().then(({ done, value }) => {
                if (done) {
                    console.log('Stream complete');
                    return;
                }
                
                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split('\n');
                
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.substring(6));
                            
                            if (data.type === 'start') {
                                console.log('开始生成报告:', data.kin_name);
                                // 更新进度条
                                updateProgress(0, progressTexts[0]);
                            } else if (data.type === 'content') {
                                console.log('收到内容:', data.content);
                                fullContent += data.content;
                                // 实时更新进度
                                progressStep = Math.min(progressStep + 1, progressTexts.length - 1);
                                updateProgress(progressStep / (progressTexts.length - 1), progressTexts[progressStep]);
                            } else if (data.type === 'complete') {
                                console.log('报告生成完成');
                                fullContent = data.content;
                                finishReport(fullContent);
                            }
                        } catch (e) {
                            console.error('解析数据失败:', e);
                        }
                    }
                }
                
                return readStream();
            });
        }
        
        return readStream();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('生成报告失败，请重试');
        document.getElementById('loadingOverlay').classList.remove('active');
        document.getElementById('submitBtn').disabled = false;
    });
}