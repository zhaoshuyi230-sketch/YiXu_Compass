// Edge Runtime API Route - 突破 Vercel 10 秒限制
export const runtime = 'edge';

// CORS 头
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

// 玛雅印记数据
const kinData = {
  1: { name: '红龙', emoji: '🐉' },
  2: { name: '白风', emoji: '🌬️' },
  3: { name: '蓝夜', emoji: '🌙' },
  4: { name: '黄种子', emoji: '🌱' },
  5: { name: '红蛇', emoji: '🐍' },
  6: { name: '白世界桥', emoji: '🌉' },
  7: { name: '蓝手', emoji: '✋' },
  8: { name: '黄星星', emoji: '⭐' },
  9: { name: '红月', emoji: '🌕' },
  10: { name: '白狗', emoji: '🐕' },
  11: { name: '蓝猴', emoji: '🐒' },
  12: { name: '黄人', emoji: '👤' },
  13: { name: '红天行者', emoji: '🚶' },
  14: { name: '白巫师', emoji: '🧙' },
  15: { name: '蓝鹰', emoji: '🦅' },
  16: { name: '黄战士', emoji: '⚔️' },
  17: { name: '红地球', emoji: '🌍' },
  18: { name: '白镜子', emoji: '🪞' },
  19: { name: '蓝风暴', emoji: '⛈️' },
  20: { name: '黄太阳', emoji: '☀️' }
};

// 计算玛雅印记
function calculateKin(year, month, day) {
  const baseDate = new Date(1900, 0, 1);
  const targetDate = new Date(year, month - 1, day);
  const diffDays = Math.floor((targetDate - baseDate) / (1000 * 60 * 60 * 24));
  const kinNumber = ((diffDays % 260) + 260) % 260 + 1;
  return kinNumber;
}

// 生成系统提示词
function generateSystemPrompt(kinName, kinNumber) {
  return `你是一位世界顶级的灵性财富教练和荣格心理学大师，精通古玛雅历法与现代商业变现的底层逻辑。

请为玛雅印记【KIN ${kinNumber} ${kinName}】生成一份极具洞察力的《个人商业出厂说明书》。

**语气要求**：
- 一针见血、犀利不爹味、带有神秘的高级感
- 像一位看透人性的顶尖商业顾问
- 绝对禁止说"建立个人品牌"、"做MVP"这种正确的废话

**必须包含的板块**：
1. 🌌 五大财富能量阵（主图腾、指引图腾、支持图腾、挑战图腾、隐藏图腾）
2. 🧬 核心商业基因解码（搞钱超能力 + 致命漏财点）
3. 🚫 绝不可碰的商业红线（3条具体场景）
4. 🤝 天作之合与避坑合伙人
5. 🚀 顺势而为的13天破局行动（Day 1-7，Day 8-13标记为需解锁）

**输出格式**：使用 Markdown 格式，适当使用 Emoji 增加视觉吸引力。`;
}

// 流式生成报告
async function* streamReport(kinName, kinNumber, apiKey) {
  const systemPrompt = generateSystemPrompt(kinName, kinNumber);
  
  try {
    const response = await fetch('https://api.deepseek.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: 'deepseek-chat',
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: `请为玛雅印记【${kinName}】生成专属的《个人商业出厂说明书》。` }
        ],
        stream: true,
        temperature: 0.8,
        max_tokens: 4000
      })
    });

    if (!response.ok) {
      throw new Error(`API 请求失败: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullContent = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.substring(6);
          if (data === '[DONE]') continue;
          
          try {
            const parsed = JSON.parse(data);
            const content = parsed.choices?.[0]?.delta?.content;
            if (content) {
              fullContent += content;
              yield { type: 'content', content };
            }
          } catch (e) {
            // 忽略解析错误
          }
        }
      }
    }

    yield { type: 'complete', content: fullContent };
  } catch (error) {
    console.error('Stream error:', error);
    yield { type: 'error', message: error.message };
  }
}

// 保底内容
function getFallbackContent(kinName, kinNumber) {
  return `# 🌟 艺序 · 商业潜能解码器

## 你的专属印记：KIN ${kinNumber} ${kinName}

> "宇宙正在向你传递财富信号..."

### 🌌 五大财富能量阵

- **主图腾**：${kinName} - 天生的财富创造者
- **指引图腾**：宇宙能量指引你前行
- **支持图腾**：隐藏的支持力量正在觉醒
- **挑战图腾**：转化挑战为机遇
- **隐藏图腾**：深藏的潜能等待释放

### 🧬 核心商业基因解码

**你的搞钱超能力**：
${kinName}印记的你拥有独特的商业直觉，能够洞察他人看不到的机会。

**你最致命的漏财点**：
过于追求完美，错失最佳时机。

### 🚫 绝不可碰的商业红线

1. 🧨 **重资产投入** - 轻资产才是你的主场
2. 🧨 **单打独斗** - 你需要互补的合伙人
3. 🧨 **忽视直觉** - 你的第六感是最大财富

### 🚀 13天破局行动

**Day 1-3：能量校准**
- 清理物理和数字空间
- 列出你的3个核心技能

**Day 4-7：价值显化**
- 设计你的最小可行性产品
- 发布第一条价值内容

---

🔒 **Day 8-13 核心收割行动**
*输入激活码解锁完整版报告*

---

*本报告由艺序 AI 实验室生成*
*微信搜索：【艺序·AI创业实战】*`;
}

export default async function handler(request) {
  // 处理 CORS 预检请求
  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }

  try {
    const { year, month, day } = await request.json();
    
    if (!year || !month || !day) {
      return new Response(JSON.stringify({ error: '请提供完整的日期' }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    // 计算玛雅印记
    const kinNumber = calculateKin(parseInt(year), parseInt(month), parseInt(day));
    const kinInfo = kinData[((kinNumber - 1) % 20) + 1];
    const kinName = kinInfo?.name || '红龙';

    const apiKey = process.env.DEEPSEEK_API_KEY || process.env.OPENAI_API_KEY;
    
    if (!apiKey) {
      // 返回保底内容
      const fallbackContent = getFallbackContent(kinName, kinNumber);
      return new Response(
        JSON.stringify({ 
          type: 'complete', 
          content: fallbackContent,
          kin_name: kinName,
          kin_number: kinNumber
        }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // 创建流式响应
    const stream = new ReadableStream({
      async start(controller) {
        try {
          // 发送开始信号
          controller.enqueue(
            new TextEncoder().encode(
              JSON.stringify({ 
                type: 'start', 
                kin_name: kinName, 
                kin_number: kinNumber 
              }) + '\n'
            )
          );

          // 流式生成内容
          for await (const chunk of streamReport(kinName, kinNumber, apiKey)) {
            controller.enqueue(
              new TextEncoder().encode(JSON.stringify(chunk) + '\n')
            );
          }

          controller.close();
        } catch (error) {
          console.error('Stream error:', error);
          controller.enqueue(
            new TextEncoder().encode(
              JSON.stringify({ 
                type: 'error', 
                message: '宇宙信号波动，请重新测算',
                fallback: getFallbackContent(kinName, kinNumber)
              }) + '\n'
            )
          );
          controller.close();
        }
      }
    });

    return new Response(stream, {
      headers: {
        ...corsHeaders,
        'Content-Type': 'application/x-ndjson',
        'Cache-Control': 'no-cache'
      }
    });

  } catch (error) {
    console.error('Handler error:', error);
    return new Response(
      JSON.stringify({ error: '宇宙信号波动，请重新测算' }),
      { 
        status: 500, 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      }
    );
  }
}
