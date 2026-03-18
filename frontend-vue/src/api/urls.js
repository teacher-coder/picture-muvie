const DjangoBase = import.meta.env.VITE_API_URL

export default {
  Django_API: `${DjangoBase}api/`,

  getLyrics: 'lyrics',
  downloadLyricsDocx: 'makedocx',
}
