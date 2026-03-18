import Header from "./components/Header";
import Home from "./components/Home";
import Footer from "./components/Footer";

export default function App() {
  return (
    <div className="mx-auto flex min-h-screen max-w-2xl flex-col px-6 sm:px-8">
      <Header />
      <main className="flex-1 pb-16">
        <Home />
      </main>
      <Footer />
    </div>
  );
}
