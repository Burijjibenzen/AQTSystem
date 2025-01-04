import axios from 'axios'

const axiosInstance = axios.create({
    //baseURL: 'http://localhost:3000' // 配置baseURL
    baseURL: '' // 配置baseURL
})

export default axiosInstance


//axios没搞成功，先传这一版吧，下一版把axios搞明白
