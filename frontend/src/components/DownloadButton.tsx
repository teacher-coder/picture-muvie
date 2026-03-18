import { useState, useRef, useEffect } from "react";
import IconChevron from "../icons/IconChevron";

interface DownloadItem {
  name: string;
  onClicked: () => void;
}

interface Props {
  name: string;
  items: DownloadItem[];
}

export default function DownloadButton({ name, items }: Props) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div ref={ref} className="relative inline-flex">
      <button
        className="inline-flex items-center gap-1.5 rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition-all hover:bg-primary-hover active:scale-[0.98]"
        onClick={() => setOpen(!open)}
      >
        {name}
        <IconChevron className={`transition-transform ${open ? "rotate-180" : ""}`} />
      </button>
      {open && (
        <div className="absolute bottom-full right-0 mb-2 w-full min-w-[120px] overflow-hidden rounded-lg border border-border bg-white shadow-lg">
          {items.map((item, i) => (
            <button
              key={i}
              className="block w-full px-4 py-2.5 text-left text-sm font-medium text-text transition-colors hover:bg-surface-alt"
              onClick={() => {
                item.onClicked();
                setOpen(false);
              }}
            >
              {item.name}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
