import { For, Show } from "solid-js";
import "./features.css";

// Define a type for the features
type Feature = {
  icon: string;
  title: string;
  description: string;
};

// Declare the features array with type annotations
const features: Feature[] = [
  {
    icon: "🧠",
    title: "Automatic Conversion",
    description: "Convert PDFs to mind maps in seconds.",
  },
  {
    icon: "🎨",
    title: "Customizable Maps",
    description: "Personalize your mind maps with ease.",
  },
  {
    icon: "📂",
    title: "Export Options",
    description: "Export your mind maps to various formats.",
  },
];

const FeaturesOverview = () => {
  return (
    <div class="featureBox">
    <Show when={features.length > 0}>
      <div class="features-overview">
        <For each={features}>
          {(feature: Feature, index) => (
            <div class="feature">
              <span class="icon">{feature.icon}</span>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </div>
          )}
        </For>
      </div>
    </Show>
    </div>
  );
};

export default FeaturesOverview;
