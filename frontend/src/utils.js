function downloadFile(data, fileName) {
  const url = URL.createObjectURL(new Blob([data]))
  const link = document.createElement('a')
  document.body.appendChild(link)
  link.href = url
  link.hidden = true
  link.setAttribute('download', fileName)
  link.click()
  document.body.removeChild(link)
  link.remove()
}

export { downloadFile }

// 한글 체크
function isHangeul(str) {
  const regExp = /[ㄱ-ㅎㅏ-ㅣ가-힣]/g
  if (regExp.test(str)) {
    return true
  } else {
    return false
  }
}

// 영문(영어) 체크
function isAlphabet(str) {
  const regExp = /[a-zA-Z]/g // 영어
  if (regExp.test(str)) {
    return true
  } else {
    return false
  }
}

// 공백(스페이스 바) 체크
function isSpace(str) {
  if (str.search(/\s/) !== -1) {
    return true // 스페이스가 있는 경우
  } else {
    return false // 스페이스 없는 경우
  }
}

function countLyricType(lyric) {
  let chr_dict = { alphabet: 0, hangeul: 0, space: 0, special: 0 }
  for (let c of lyric) {
    if (isAlphabet(c)) {
      chr_dict['alphabet'] += 1
    } else if (isHangeul(c)) {
      chr_dict['hangeul'] += 1
    } else if (isSpace(c)) {
      chr_dict['space'] += 1
    } else {
      chr_dict['special'] += 1
    }
  }
  return chr_dict
}

function getUnitLength(lyric) {
  let chr_dict = countLyricType(lyric)
  return (
    chr_dict['alphabet'] * 0.6 +
    chr_dict['hangeul'] +
    chr_dict['space'] +
    chr_dict['special'] * 0.4
  )
}

function compressLyrics(lyric_text, buffer_offset = 25) {
  let result = ''
  let buffer = ''
  let buffer_length = 0
  let idx = 0

  const lyrics_list = lyric_text.split('\n').map(str => str.trim())

  while (idx < lyrics_list.length) {
    if (lyrics_list[idx] === '') {
      if (buffer === '') {
        idx++
      } else {
        if (buffer !== '') {
          result += buffer
        }
        buffer = ''
        buffer_length = 0
      }
      result += '\n\n'
    } else {
      buffer_length += getUnitLength(lyrics_list[idx])
      if (buffer_length > buffer_offset) {
        if (buffer !== '') {
          result += buffer + '\n'
        }
        buffer = lyrics_list[idx]
        buffer_length = getUnitLength(lyrics_list[idx])
      } else {
        if (buffer !== '') {
          buffer = buffer + ' ' + lyrics_list[idx]
        } else {
          buffer = lyrics_list[idx]
        }
      }
    }
    if (idx === lyrics_list.length - 1 && buffer !== '') {
      result += buffer
    }
    idx++
  }
  return result.trim()
}

export { compressLyrics }
