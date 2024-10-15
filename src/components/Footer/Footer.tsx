import "./footer.css";
import fb from "../../assets/fb.png"
import X from "../../assets/X.png"
import wa from "../../assets/wa.png"

const Footer = () => {
  return (
    <footer class="footer">
      <div class="footer-left">
        <h3 class="company-name">TopicNet</h3>
        <p class="compnay-data">Transforming pdfs to mind maps</p>
      </div>
      <div class="footer-right">
        <h4>Contact us</h4>
        <div class="social-icons">
          <a href="#" aria-label="Facebook" class="icon facebook"><img class="sm-icon" src={fb} alt="facebook" /></a>
          <a href="#" aria-label="Twitter" class="icon twitter"><img class="sm-icon" src={X} alt="facebook" /></a>
          <a href="#" aria-label="Instagram" class="icon whatsapp"><img class="sm-icon" src={wa} alt="facebook" /></a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
