export function downloadFile(data: Blob, fileName: string) {
  const url = URL.createObjectURL(new Blob([data]));
  const link = document.createElement("a");
  document.body.appendChild(link);
  link.href = url;
  link.hidden = true;
  link.setAttribute("download", fileName);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function isHangeul(str: string): boolean {
  return /[ㄱ-ㅎㅏ-ㅣ가-힣]/.test(str);
}

function isAlphabet(str: string): boolean {
  return /[a-zA-Z]/.test(str);
}

function isSpace(str: string): boolean {
  return /\s/.test(str);
}

function getUnitLength(lyric: string): number {
  let alphabet = 0,
    hangeul = 0,
    space = 0,
    special = 0;
  for (const c of lyric) {
    if (isAlphabet(c)) alphabet++;
    else if (isHangeul(c)) hangeul++;
    else if (isSpace(c)) space++;
    else special++;
  }
  return alphabet * 0.6 + hangeul + space + special * 0.4;
}

export function compressLyrics(
  lyricText: string,
  bufferOffset: number = 25
): string {
  let result = "";
  let buffer = "";
  let bufferLength = 0;
  let idx = 0;

  const lyricsList = lyricText
    .trim()
    .split("\n")
    .map((str) => str.trim());

  while (idx < lyricsList.length) {
    if (lyricsList[idx] === "") {
      if (buffer === "") {
        idx++;
      } else {
        result += buffer;
        buffer = "";
        bufferLength = 0;
      }
      result += "\n\n";
    } else {
      bufferLength += getUnitLength(lyricsList[idx]);
      if (bufferLength > bufferOffset) {
        if (buffer !== "") {
          result += buffer + "\n";
        }
        buffer = lyricsList[idx];
        bufferLength = getUnitLength(lyricsList[idx]);
      } else {
        buffer = buffer !== "" ? buffer + " " + lyricsList[idx] : lyricsList[idx];
      }
    }
    if (idx === lyricsList.length - 1 && buffer !== "") {
      result += buffer;
    }
    idx++;
  }
  return result.trim();
}
