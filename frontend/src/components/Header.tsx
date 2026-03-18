import IconMovie from "../icons/IconMovie";

export default function Header() {
  return (
    <nav className="flex items-center justify-between border-b border-border py-5">
      <a href="/" className="flex items-center gap-3 transition-opacity hover:opacity-70">
        <IconMovie />
        <span className="text-lg font-semibold tracking-tight text-text">
          그림 뮤비 제작
        </span>
      </a>
      <div className="flex items-center gap-5 text-sm font-medium text-text-muted">
        <a
          href="https://extreme-pipe-53e.notion.site/PicMuvie-fca423162623449197924c80b68f942d"
          target="_blank"
          rel="noreferrer"
          className="transition-colors hover:text-text"
        >
          About
        </a>
        <a
          href="https://github.com/teacher-coder/picture-muvie"
          target="_blank"
          rel="noreferrer"
          className="transition-colors hover:text-text"
        >
          GitHub
        </a>
      </div>
    </nav>
  );
}
