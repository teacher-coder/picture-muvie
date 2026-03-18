import { useState, useRef, useEffect } from "react";

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
    <div ref={ref} className="relative">
      <button
        className="bg-rose-600 px-6 py-2 font-bold text-white hover:bg-rose-800"
        onClick={() => setOpen(!open)}
      >
        {name} ▲
      </button>
      {open && (
        <div className="absolute bottom-full right-0 mb-2 space-y-1">
          {items.map((item, i) => (
            <button
              key={i}
              className="block w-full bg-rose-600 px-10 py-2 text-sm text-white hover:bg-rose-800"
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
