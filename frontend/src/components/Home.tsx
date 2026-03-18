import { useState, useRef, type FormEvent } from "react";
import { getLyrics, downloadLyricsDocx } from "../api/lyrics";
import { compressLyrics, downloadFile } from "../utils";
import DownloadButton from "./DownloadButton";
import LyricsCard from "./LyricsCard";
import MergeButton from "./MergeButton";
import IconSpinner from "../icons/IconSpinner";

export default function Home() {
  const [query, setQuery] = useState("");
  const [searching, setSearching] = useState(false);
  const [lines, setLines] = useState<string[]>([]);
  const [lyricsSource, setLyricsSource] = useState("");
  const [error, setError] = useState("");

  const lyricsTitle = useRef("");
  const lyricsArtist = useRef("");
  const defaultOffset = useRef(30);



  function textToLines(text: string): string[] {
    return text.split("\n").filter((n) => n);
  }

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


  function handleCardChange(index: number, text: string) {
    if (!text) {
      setLines((prev) => prev.filter((_, i) => i !== index));
    } else {
      setLines((prev) => prev.map((l, i) => (i === index ? text : l)));
    }
  }

  function handleMergeWithPrev(index: number) {
    if (index === 0) return;
    setLines((prev) => {
      const merged = prev[index - 1] + " " + prev[index];
      return prev
        .filter((_, i) => i !== index)
        .map((l, i) => (i === index - 1 ? merged : l));
    });
  }

  function handleMergeAt(index: number) {
    setLines((prev) => {
      const merged = prev[index] + " " + prev[index + 1];
      return prev
        .filter((_, i) => i !== index + 1)
        .map((l, i) => (i === index ? merged : l));
    });
  }

  function handleSplitAtCursor(index: number, before: string, after: string) {
    setLines((prev) => [
      ...prev.slice(0, index),
      before,
      after,
      ...prev.slice(index + 1),
    ]);
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

      let resultText: string;
      if (lineLength > 24) {
        setDefaultOffsetValue(lyricText);
        resultText = compressLyrics(lyricText, defaultOffset.current);
      } else {
        resultText = lyricText;
      }

      setLines(textToLines(resultText));
      setLyricsSource(response.source);
      lyricsTitle.current = response.title;
      lyricsArtist.current = response.artist;
    } catch {
      setLines(["검색에 실패했습니다. 잠시 후 다시 시도해주세요."]);
    } finally {
      setSearching(false);
    }
  }

  async function handleDownload(ext: string) {
    const blob = await downloadLyricsDocx(lyricsTitle.current, lines);
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
            {searching ? <IconSpinner /> : null}
            {searching ? "검색 중" : "검색"}
          </button>
        </div>
        {error && <p className="text-sm text-primary">{error}</p>}
      </form>

      {/* Lyrics cards */}
      <div className="flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold text-text-muted">
            가사 편집
            {lines.length > 0 && (
              <span className="ml-2 text-xs font-normal text-text-muted/60">
                클릭해서 편집 · 가위로 나누기
              </span>
            )}
          </h2>
        </div>

        {lines.length > 0 ? (
          <div className="flex flex-col">
            {lines.map((line, i) => (
              <div key={`${i}-${line.slice(0, 20)}`}>
                <LyricsCard
                  line={line}
                  index={i}
                  onChange={handleCardChange}
                  onMergeWithPrev={handleMergeWithPrev}
                  onSplitAtCursor={handleSplitAtCursor}
                />
                {i < lines.length - 1 && (
                  <MergeButton onClick={() => handleMergeAt(i)} />
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center rounded-lg border border-dashed border-border py-16 text-center">
            <p className="text-sm text-text-muted">
              가사를 검색하면 여기에 카드로 표시됩니다
            </p>
            <p className="mt-1 text-xs text-text-muted/60">
              카드를 클릭해서 편집하고, Enter로 줄을 나눌 수 있어요
            </p>
          </div>
        )}

        <div className="flex items-center justify-between text-sm text-text-muted">
          <span>{lyricsSource ? `출처: ${lyricsSource}` : ""}</span>
          <span className="font-medium tabular-nums">
            학급 인원: <span className="text-text">{lines.length}명</span>
          </span>
        </div>
        <div className="flex justify-end">
          <DownloadButton name="다운로드" items={downloadItems} />
        </div>
      </div>
    </div>
  );
}
