import axios from 'axios'
import urls from '@/api/urls'

function createAxiosInstance(baseUrl, timeOut) {
  const axiosInstance = axios.create({
    baseURL: baseUrl,
    timeout: timeOut,
  })
  return axiosInstance
}

function setInterceptors(axiosInstance) {
  axiosInstance.interceptors.request.use(
    function (config) {
      return config
    },
    function (error) {
      return Promise.reject(error)
    }
  )

  axiosInstance.interceptors.response.use(
    function (response) {
      return response
    },
    function (error) {
      console.log('Error :', error.response)
      return Promise.reject(error.response)
    }
  )

  return axiosInstance
}

const myAxios = setInterceptors(createAxiosInstance(urls.Django_API, 3000))

export default myAxios
