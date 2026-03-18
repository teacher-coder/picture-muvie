const navigation = [
  {
    name: "About",
    href: "https://extreme-pipe-53e.notion.site/PicMuvie-fca423162623449197924c80b68f942d",
  },
  {
    name: "GitHub",
    href: "https://github.com/teacher-coder/picture-muvie",
  },
];

export default function Footer() {
  return (
    <footer className="border-t border-border py-6">
      <div className="flex items-center justify-between text-sm text-text-muted">
        <span>&copy; {new Date().getFullYear()} PicMuvie</span>
        <nav className="flex gap-5" aria-label="Footer">
          {navigation.map((item) => (
            <a
              key={item.name}
              href={item.href}
              target="_blank"
              rel="noreferrer"
              className="transition-colors hover:text-text"
            >
              {item.name}
            </a>
          ))}
        </nav>
      </div>
    </footer>
  );
}
