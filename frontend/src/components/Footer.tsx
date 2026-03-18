const navigation = [
  {
    name: "About Us",
    href: "https://extreme-pipe-53e.notion.site/PicMuvie-fca423162623449197924c80b68f942d",
  },
  {
    name: "Github",
    href: "https://github.com/teacher-coder/picture-muvie",
  },
];

export default function Footer() {
  return (
    <footer className="bg-white">
      <div className="mx-auto overflow-hidden px-4 py-4 sm:px-6 lg:px-8">
        <nav
          className="-mx-5 -my-2 flex flex-wrap justify-center"
          aria-label="Footer"
        >
          {navigation.map((item) => (
            <div key={item.name} className="px-5 py-2">
              <a
                href={item.href}
                target="_blank"
                rel="noreferrer"
                className="text-base text-gray-500 hover:text-gray-900"
              >
                {item.name}
              </a>
            </div>
          ))}
        </nav>
      </div>
    </footer>
  );
}
