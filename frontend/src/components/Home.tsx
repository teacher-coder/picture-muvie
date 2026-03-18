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
      setError("노래 제목을 입력해주세요");
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
      setLyricsText("검색에 실패했습니다. 잠시 후 다시 시도해주세요.");
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
    <div className="mt-10 flex flex-col gap-10">
      {/* Hero section */}
      <div className="text-center">
        <h1 className="-tracking-wide text-3xl font-bold sm:text-4xl">
          노래 가사를 검색하고
          <br />
          <span className="text-primary">학급 인원</span>에 맞게 나눠보세요
        </h1>
        <p className="mt-3 text-text-muted">
          가사를 검색한 뒤, 학생 수에 맞게 조정하고 문서로 다운로드하세요
        </p>
      </div>

      {/* Search */}
      <form className="flex flex-col gap-3" onSubmit={handleSearch}>
        <label htmlFor="query" className="text-sm font-semibold text-text-muted">
          가사 검색
        </label>
        <div className="flex gap-2">
          <input
            id="query"
            name="query"
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              if (error) setError("");
            }}
            className="flex-1 rounded-lg border border-border bg-white px-4 py-2.5 text-sm shadow-sm transition-all placeholder:text-text-muted/50 focus:border-primary focus:ring-2 focus:ring-primary/20 focus:outline-none"
            placeholder="노래 제목과 가수 입력 (예: 출발 김동률)"
          />
          <button
            type="submit"
            disabled={searching}
            className="inline-flex items-center gap-2 rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition-all hover:bg-primary-hover active:scale-[0.98] disabled:opacity-60"
          >
            {searching ? (
              <svg
                className="h-4 w-4 animate-spin"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                />
              </svg>
            ) : null}
            {searching ? "검색 중" : "검색"}
          </button>
        </div>
        {error && (
          <p className="text-sm text-primary">{error}</p>
        )}
      </form>

      {/* Lyrics editor */}
      <div className="flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold text-text-muted">가사 편집</h2>
          <button
            className="rounded-md border border-border bg-white px-3 py-1.5 text-sm font-medium text-text shadow-sm transition-all hover:bg-surface-alt active:scale-[0.98]"
            onClick={increaseLyricsCompression}
          >
            인원 줄이기
          </button>
        </div>
        <textarea
          placeholder={
            "입력된 줄의 개수는 학생 수를 나타냅니다\nenter키를 눌러 줄을 바꾸고 학생 수를 조정해주세요"
          }
          value={lyricsText}
          onChange={(e) => setLyricsText(e.target.value)}
          rows={10}
          className="w-full rounded-lg border border-border bg-white p-4 text-sm leading-relaxed shadow-sm transition-all placeholder:text-text-muted/50 focus:border-primary focus:ring-2 focus:ring-primary/20 focus:outline-none"
        />
        <div className="flex items-center justify-between text-sm text-text-muted">
          <span>{lyricsSource ? `출처: ${lyricsSource}` : ""}</span>
          <span className="font-medium tabular-nums">
            학급 인원: <span className="text-text">{lyricsList.length}명</span>
          </span>
        </div>
        <div className="flex justify-end">
          <DownloadButton name="다운로드" items={downloadItems} />
        </div>
      </div>
    </div>
  );
}
