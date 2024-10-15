import { useNavigate } from "@solidjs/router";
import { createEffect, createSignal } from "solid-js";
import Footer from "../../components/Footer/Footer";
import Navbar from "../../components/Navbar/Navbar";
import { useUserContext } from "../../context/UserContext";
import "./uploadPage.css";

const UploadPage = () => {
  const navigate = useNavigate();
  const { username, setUsername } = useUserContext(); // Accessing username from UserContext

  // createEffect(() => {
  //   const verifyToken = async () => {
  //     const token = localStorage.getItem('token');
  //       console.log(token)
  //     try {
  //       const response = await fetch(`http://localhost:8000/verify-token/${token}`);

  //       if (!response.ok) {
  //         throw new Error('Token verification failed');
  //       }
  //     } catch (error) {
  //       localStorage.removeItem('token');
  //       navigate('/login');
  //     }
  //   };

  //   verifyToken();
  // }, [navigate]);

  const handleSubmit = async (event: Event) => {
    event.preventDefault();

    const token = localStorage.getItem("token");
    if (!token) {
      // Redirect to login if the token is missing
      navigate("/login");
      return;
    }

    try {
      const response = await fetch(
        `http://localhost:8000/verify-token/${token}`
      );
      if (!response.ok) {
        throw new Error("Token verification failed");
      }
    } catch (error) {
      localStorage.removeItem("token");
      navigate("/login");
      return;
    }

    if (!selectedFile()) {
      setMessage("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile() as File);

    try {
      const response = await fetch(
        `http://localhost:8000/uploadfile/${username()}`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (response.ok) {
        const data = await response.json();
        localStorage.removeItem("file_path");
        localStorage.setItem("file_path", data.file_path);

        setMessage("File uploaded successfully!");
        navigate("/board");
      } else {
        setMessage("Failed to upload file.");
      }
    } catch (error) {
      setMessage("An error occurred. Please try again.");
    }
  };

  let inputRef: HTMLInputElement | undefined;

  const [selectedFile, setSelectedFile] = createSignal<File | null>(null);
  const [fileText, setFileText] = createSignal<string>("");
  const [isGenerating, setIsGenerating] = createSignal<boolean>(false);
  const [mindMapRendered, setMindMapRendered] = createSignal<boolean>(false);

  // const [file, setFile] = createSignal<File | null>(null);
  const [message, setMessage] = createSignal("");

  createEffect(() => {
    inputRef?.focus();
  });

  const handleOnChange = (event: Event & { target: HTMLInputElement }) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      setSelectedFile(files[0]);
      setMindMapRendered(false);
    }
  };

  const onChooseFile = () => {
    inputRef?.click();
  };

  const removeFile = () => {
    setSelectedFile(null);
    setFileText("");
    setIsGenerating(false);
    setMindMapRendered(false);
  };

  // const readFile = async () => {
  //   const file = selectedFile();

  //   if (file) {
  //     setIsGenerating(true);
  //     const reader = new FileReader();
  //     reader.onload = async (e) => {
  //       const text = e.target?.result as string;
  //       setFileText(text);
  //       // await generateMap(text);
  //       setIsGenerating(false);
  //       setMindMapRendered(true);
  //     };

  //     reader.readAsText(file);
  //   }
  // };

  //   const generateMap = async (text: string) => {
  //     if (text) {
  //     //   const { graphviz } = await import("d3-graphviz");
  //       graphviz("#graph").renderDot(text);
  //     }
  //   };

  // const handleSubmit = async (event: Event) => {
  //   event.preventDefault();

  //   if (!selectedFile()) {
  //     setMessage("Please select a file to upload.");
  //     return;
  //   }

  //   const formData = new FormData();
  //   formData.append("file", selectedFile() as File);

  //   try {
  //     const response = await fetch(
  //       `http://localhost:8000/uploadfile/${username()}`,
  //       {
  //         method: "POST",
  //         body: formData,
  //       }
  //     );

  //     if (response.ok) {
  //       const data = await response.json();
  //       localStorage.removeItem("file_path");
  //       localStorage.setItem("file_path", data.file_path);

  //       setMessage("File uploaded successfully!");
  //       navigate("/board");
  //     } else {
  //       setMessage("Failed to upload file.");
  //     }
  //   } catch (error) {
  //     setMessage("An error occurred. Please try again.");
  //   }
  // };

  return (
    <>
      <Navbar />
      <div class="uploadPage">
        <div class="center">
          <span class="uploadTitle">Upload Document</span>
          <br />
          <span class="uploadTxt">
            Upload your document and let the mind map be generated!
          </span>

          <div class="uploadBox">
            {!selectedFile() && (
              <input
                type="file"
                ref={(el) => (inputRef = el)}
                onChange={handleOnChange}
                style={{ display: "none" }}
              />
            )}

            {!selectedFile() && (
              <button class="file-btn" onClick={onChooseFile}>
                Click to upload file
              </button>
            )}
          </div>
          <form onSubmit={handleSubmit}>
            {selectedFile() && (
              <div class="selected-file">
                <p>{selectedFile()?.name}</p>
                <button onClick={removeFile}>🗑</button>
              </div>
            )}

            {selectedFile() && (
              <button type="submit" class={`generateBtn`}>
                Generate Mind Map
              </button>
            )}
          </form>
          {message && <p>{message()}</p>}

          {isGenerating() && (
            <span class="generating-txt">Generating your mind map...</span>
          )}

          {mindMapRendered() && (
            <>
              <h2 class="mindMapTitle">Your Mind Map</h2>
              <div id="graph"></div>
            </>
          )}
        </div>
        <div class="howItWorks">
          <h2>How TopicNet Works</h2>
          <p>
            Here is how your PDF is converted to a mind map by our application:
          </p>
          <ol>
            <li>Extract and Clean Text in the PDF</li>
            <li>Embed and Reduce Cleaned Text to Create Summaries</li>
            <li>Cluster Embedded Text based on Content</li>
            <li>Generate Topics for each Cluster identified</li>
            <li>Finetune the content with LLMs</li>
            <li>Display the Topics and Content in a Mind Map</li>
          </ol>
          <br />
          <p>
            We use <b>hightly tested, cutting-edge AI and LLM models</b> to read
            your PDF and genetare mind maps:
          </p>
          <ul>
            <li>Existing Libraries for Text Extraction</li>
            <li>Rule-based approach for Text Cleaning</li>
            <li>Sentence Transformers for Text Embedding</li>
            <li>UMAP for Dimensionality Reduction</li>
            <li>HDBScan for Text Clustering</li>
            <li>Count Vectorizer + TF-IDF for Topic Generation</li>
            <li>LLMs for finetuning topics and corresponding content</li>
          </ul>
        </div>
      </div>
      <Footer />
    </>
  );
};

export default UploadPage;
