import myAxios from '@/api/SetAxios'
import urls from '@/api/urls'

export default {
  async getLyrics(...params) {
    return myAxios
      .get(urls.getLyrics, ...params)
      .then((response) => response.data)
  },
  async downloadLyricsDocx(...params) {
    return myAxios
      .post(urls.downloadLyricsDocx, ...params)
      .then((response) => response.data)
  },
}
