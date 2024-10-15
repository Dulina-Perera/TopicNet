// import FeaturesOverview from "../../components/features/Features";
import { useNavigate } from "@solidjs/router";
import FeaturesOverview from "../../components/Features/Features";
import Footer from "../../components/Footer/Footer";
import Navbar from "../../components/Navbar/Navbar";
import About from "../AboutPage/About";
import "./homePage.css";

function Home() {
  const navigate = useNavigate();

  const navigateToUpload = () => {
    navigate("/upload");
  };

  return (
    <>
      <Navbar />
      <div class="homePage">
        <span class="text1">Content summarization, redefined.</span>
        <br />
        <div class="text2">
          <span>
            Transform your document into a simple interactive mind map
          </span>
        </div>

        <div class="btnContainer">
          <div class="uploadBtn" onClick={navigateToUpload}>
            Upload a document
          </div>
        </div>
      </div>
      <FeaturesOverview />
      <About />
      <Footer />
    </>
  );
}

export default Home;
