import { useState, useMemo, useRef, type FormEvent } from "react";
import { getLyrics, downloadLyricsDocx } from "../api/lyrics";
import { compressLyrics, downloadFile } from "../utils";
import DownloadButton from "./DownloadButton";

export default function Home() {
  const [query, setQuery] = useState("");
  const [searching, setSearching] = useState(false);
  const [lyricsText, setLyricsText] = useState("");
  const [lyricsSource, setLyricsSource] = useState("");
  const [error, setError] = useState("");

  const lyricsTitle = useRef("");
  const lyricsArtist = useRef("");
  const defaultOffset = useRef(30);

  const lyricsList = useMemo(
    () => lyricsText.split("\n").filter((n) => n),
    [lyricsText]
  );

  const minLineLength = useMemo(
    () => lyricsText.split("\n\n").length,
    [lyricsText]
  );

  function setDefaultOffsetValue(lyricText: string) {
    let offset = 30;
    while (
      compressLyrics(lyricText, offset).split("\n").filter((n) => n).length <
        24 &&
      offset > 0
    ) {
      offset--;
    }
    defaultOffset.current = offset;
  }

  function increaseLyricsCompression() {
    if (!lyricsText) return;
    let compressOffset = defaultOffset.current;
    const curLineLength = lyricsList.length;
    let newText = lyricsText;
    while (
      newText.split("\n").filter((n) => n).length === curLineLength
    ) {
      if (curLineLength === minLineLength) break;
      compressOffset += 1;
      newText = compressLyrics(lyricsText, compressOffset);
    }
    defaultOffset.current = compressOffset;
    setLyricsText(newText);
  }

  async function handleSearch(e: FormEvent) {
    e.preventDefault();
    if (!query.trim()) {
      setError("필수로 입력해야 합니다");
      return;
    }
    setError("");
    setSearching(true);
    defaultOffset.current = 30;

    try {
      const response = await getLyrics(query);
      const lyricText = response.lyrics;
      const lineLength = lyricText.split("\n").filter((n) => n).length;

      if (lineLength > 24) {
        setDefaultOffsetValue(lyricText);
        setLyricsText(compressLyrics(lyricText, defaultOffset.current));
      } else {
        setLyricsText(lyricText);
      }

      setLyricsSource(response.source);
      lyricsTitle.current = response.title;
      lyricsArtist.current = response.artist;
    } catch {
      setLyricsText("에러가 발생했습니다. 다음에 다시 시도해주세요.");
    } finally {
      setSearching(false);
    }
  }

  async function handleDownload(ext: string) {
    const blob = await downloadLyricsDocx(lyricsTitle.current, lyricsList);
    const fileName =
      (lyricsTitle.current + "-" + lyricsArtist.current || "lyrics") + ext;
    downloadFile(blob, fileName);
  }

  const downloadItems = [
    { name: "Hwp", onClicked: () => handleDownload(".hwp") },
    { name: "Docx", onClicked: () => handleDownload(".docx") },
  ];

  return (
    <div className="my-5 flex w-full flex-col space-y-5">
      <form className="flex flex-col space-y-3" onSubmit={handleSearch}>
        <label htmlFor="query" className="text-xl font-bold">
          가사 찾기
        </label>
        <div className="flex flex-col">
          <input
            name="query"
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="rounded-lg border border-solid border-gray-300 bg-gray-50 p-2.5"
            placeholder="노래 제목과 가수 입력 - 예시) 출발 김동률, ditto newjeans"
          />
          {error && <span className="text-red-700">{error}</span>}
        </div>
        <button
          type="submit"
          className="flex justify-center rounded-md bg-rose-600 py-1 font-bold text-white hover:bg-rose-800"
          disabled={searching}
        >
          {searching ? (
            <svg
              className="h-5 w-5 animate-spin"
              fill="currentColor"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 512 512"
            >
              <path d="M126.9 142.9c62.2-62.2 162.7-62.5 225.3-1L311 183c-6.9 6.9-8.9 17.2-5.2 26.2s12.5 14.8 22.2 14.8H447.5c0 0 0 0 0 0H456c13.3 0 24-10.7 24-24V72c0-9.7-5.8-18.5-14.8-22.2s-19.3-1.7-26.2 5.2L397.4 96.6c-87.6-86.5-228.7-86.2-315.8 1C57.2 122 39.6 150.7 28.8 181.4c-5.9 16.7 2.9 34.9 19.5 40.8s34.9-2.9 40.8-19.5c7.7-21.8 20.2-42.3 37.8-59.8zM0 312v7.6 .7V440c0 9.7 5.8 18.5 14.8 22.2s19.3 1.7 26.2-5.2l41.6-41.6c87.6 86.5 228.7 86.2 315.8-1c24.4-24.4 42.1-53.1 52.9-83.7c5.9-16.7-2.9-34.9-19.5-40.8s-34.9 2.9-40.8 19.5c-7.7 21.8-20.2 42.3-37.8 59.8c-62.2 62.2-162.7 62.5-225.3 1L169 329c6.9-6.9 8.9-17.2 5.2-26.2s-12.5-14.8-22.2-14.8H32.4h-.7H24c-13.3 0-24 10.7-24 24z" />
            </svg>
          ) : (
            "검색"
          )}
        </button>
      </form>

      <div className="flex flex-col space-y-3">
        <div className="flex justify-between">
          <label className="text-xl font-bold">가사 구간 나누기</label>
          <button
            className="rounded-md border border-solid border-gray-400 px-3 py-1 font-medium text-gray-900 hover:bg-gray-50"
            onClick={increaseLyricsCompression}
          >
            인원 줄이기
          </button>
        </div>
        <textarea
          placeholder={
            "입력된 줄의 개수는 학생 수를 나타냅니다\nenter키를 눌러 줄을 바꾸고 학생 수를 조정해주세요\n아래에 학급 인원 수를 확인하실 수 있습니다"
          }
          value={lyricsText}
          onChange={(e) => setLyricsText(e.target.value)}
          rows={8}
          className="w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 focus:border-blue-500 focus:ring-blue-500"
        />
        <div className="flex justify-between">
          <div className="text-lg">출처 : {lyricsSource}</div>
          <div className="text-right text-lg">
            학급 인원 : {lyricsList.length}명
          </div>
        </div>
        <DownloadButton name="다운로드" items={downloadItems} />
      </div>
    </div>
  );
}
