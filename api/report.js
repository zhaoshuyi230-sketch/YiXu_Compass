// Vercel Serverless Function - CommonJS syntax
module.exports = function handler(req, res) {
  // 1. 强制允许跨域，防止被浏览器拦截
  res.setHeader('Access-Control-Allow-Credentials', true)
  res.setHeader('Access-Control-Allow-Origin', '*')
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT')
  res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version')

  // 2. 处理预检请求
  if (req.method === 'OPTIONS') {
    return res.status(200).end()
  }

  // 3. 处理核心 POST 请求
  if (req.method === 'POST') {
    return res.status(200).json({ message: "【后端核爆测试】API通道完全畅通！Vercel已苏醒！" })
  }

  // 4. 其他请求拦截
  return res.status(405).json({ error: "Method not allowed" })
}