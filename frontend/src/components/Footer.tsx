export default function Footer() {
  return (
    <footer className="border-t border-border py-6">
      <p className="text-center text-sm text-text-muted">
        &copy; {new Date().getFullYear()} PicMuvie
      </p>
    </footer>
  );
}
