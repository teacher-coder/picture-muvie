import IconMovie from "../icons/IconMovie";

export default function Header() {
  return (
    <nav className="flex flex-wrap items-center justify-between py-6">
      <div className="mr-6 flex items-center">
        <IconMovie />
        <span className="ml-6 text-xl font-semibold tracking-tight">
          그림 뮤비 제작
        </span>
      </div>
      <div className="block items-center">
        <a
          href="https://extreme-pipe-53e.notion.site/PicMuvie-fca423162623449197924c80b68f942d"
          target="_blank"
          rel="noreferrer"
          className="mr-4 mt-0 inline-block hover:text-red-500"
        >
          About Us
        </a>
        <a
          href="https://github.com/teacher-coder/picture-muvie"
          target="_blank"
          rel="noreferrer"
          className="mt-0 inline-block hover:text-red-500"
        >
          Github
        </a>
      </div>
    </nav>
  );
}
