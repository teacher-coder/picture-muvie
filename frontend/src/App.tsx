import Header from "./components/Header";
import Home from "./components/Home";
import Footer from "./components/Footer";

export default function App() {
  return (
    <div className="mx-auto flex min-h-screen max-w-4xl flex-col px-4">
      <Header />
      <main className="flex-1">
        <Home />
      </main>
      <Footer />
    </div>
  );
}
