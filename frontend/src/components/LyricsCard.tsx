import { useState, useRef, useEffect } from "react";
import IconScissors from "../icons/IconScissors";

interface Props {
  line: string;
  index: number;
  onChange: (index: number, text: string) => void;
  onMergeWithPrev: (index: number) => void;
  onSplitAtCursor: (index: number, before: string, after: string) => void;
}

export default function LyricsCard({
  line,
  index,
  onChange,
  onMergeWithPrev,
  onSplitAtCursor,
}: Props) {
  const [editing, setEditing] = useState(false);
  const [splitting, setSplitting] = useState(false);
  const [editValue, setEditValue] = useState(line);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    setEditValue(line);
  }, [line]);

  useEffect(() => {
    if (editing && inputRef.current) {
      inputRef.current.focus();
    }
  }, [editing]);

  function handleBlur() {
    setEditing(false);
    if (editValue.trim() !== line) {
      onChange(index, editValue.trim());
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") {
      e.preventDefault();
      const input = inputRef.current;
      if (!input) return;
      const pos = input.selectionStart ?? editValue.length;
      const before = editValue.slice(0, pos).trim();
      const after = editValue.slice(pos).trim();
      if (before && after) {
        onSplitAtCursor(index, before, after);
        setEditing(false);
      } else {
        handleBlur();
      }
    } else if (e.key === "Escape") {
      setEditValue(line);
      setEditing(false);
    } else if (
      e.key === "Backspace" &&
      inputRef.current?.selectionStart === 0 &&
      index > 0
    ) {
      e.preventDefault();
      onMergeWithPrev(index);
      setEditing(false);
    }
  }

  // Split words into clickable segments
  function splitWords(): string[] {
    return line.split(/(\s+)/).filter(Boolean);
  }

  function handleSplitAt(wordIndex: number) {
    const words = splitWords();
    const before = words.slice(0, wordIndex + 1).join("").trim();
    const after = words.slice(wordIndex + 1).join("").trim();
    if (before && after) {
      onSplitAtCursor(index, before, after);
    }
    setSplitting(false);
  }

  return (
    <div
      className={`group flex items-start gap-3 rounded-lg border px-4 py-3 transition-all duration-200 ${
        editing
          ? "border-primary/40 bg-white shadow-md ring-2 ring-primary/10"
          : splitting
            ? "border-amber-400/40 bg-white shadow-md ring-2 ring-amber-400/10"
            : "border-border bg-white shadow-sm hover:border-primary/20 hover:shadow"
      }`}
    >
      {/* Student number */}
      <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary/10 text-xs font-semibold tabular-nums text-primary">
        {index + 1}
      </span>

      {/* Content */}
      <div className="flex-1 min-w-0">
        {editing ? (
          <input
            ref={inputRef}
            type="text"
            value={editValue}
            onChange={(e) => setEditValue(e.target.value)}
            onBlur={handleBlur}
            onKeyDown={handleKeyDown}
            className="w-full border-none bg-transparent text-sm leading-relaxed text-text outline-none"
          />
        ) : splitting ? (
          <div className="flex flex-wrap items-center gap-0.5">
            <span className="mb-1 mr-2 text-[11px] text-amber-600">나눌 위치를 선택하세요</span>
            {splitWords().map((word, wi) => {
              const isSpace = /^\s+$/.test(word);
              if (isSpace) return <span key={wi}>{" "}</span>;
              return (
                <button
                  key={wi}
                  onClick={() => handleSplitAt(wi)}
                  className="rounded px-1 py-0.5 text-sm leading-relaxed text-text transition-colors hover:bg-amber-100 hover:text-amber-800"
                >
                  {word}
                </button>
              );
            })}
            <button
              onClick={() => setSplitting(false)}
              className="ml-2 text-[11px] text-text-muted hover:text-text"
            >
              취소
            </button>
          </div>
        ) : (
          <p
            className="cursor-text text-sm leading-relaxed text-text"
            onClick={() => setEditing(true)}
          >
            {line}
          </p>
        )}
      </div>

      {/* Scissors button */}
      {!editing && !splitting && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            setSplitting(true);
          }}
          className="shrink-0 rounded p-1 text-text-muted/50 transition-all duration-200 hover:bg-amber-50 hover:text-amber-600"
          title="가사 나누기"
        >
          <IconScissors />
        </button>
      )}
    </div>
  );
}
