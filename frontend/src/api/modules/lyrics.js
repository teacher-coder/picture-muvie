import myAxios from '@/api/SetAxios'
import urls from '@/api/urls'

export default {
  async getLyrics(...params) {
    return myAxios
      .get(urls.getLyrics, ...params)
      .then((response) => response.data)
  },
  async downloadLyrics(...params) {
    return myAxios
      .post(urls.downloadLyricsDocx, ...params, {
        responseType: 'blob',
        headers: {
          'Content-Type':
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        },
      })
      .then((response) => response)
  },
}
