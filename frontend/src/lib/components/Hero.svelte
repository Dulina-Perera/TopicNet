<script lang="ts">
	import { goto } from '$app/navigation';

	async function handleFileUpload(event: Event) {
		const input = event.target as HTMLInputElement;

		if (input.files && input.files.length > 0 && input.files[0].type === 'application/pdf') {
			const file: File = input.files[0];

			const formData: FormData = new FormData();
			formData.append('file_', file);

			const response = await fetch('http://localhost:5000/api/v1/generate/base', {
				method: 'POST',
				body: formData,
				credentials: 'include'
			});

			if (response.ok) {
				const data: any = await response.json();
				goto(`/${data[0].document_id}`);
			} else {
				console.error('Failed to upload file and retrieve nodes!');
			}
		}
	}
</script>

<div id="hero">
	<img src="/hero-img.svg" alt="" />
	<div id="hero-text">
		<h1>Transform Documents Into Interactive Mindmaps</h1>
		<p>
			Upload unstructured text documents like PDFs and watch them evolve into dynamic, interactive
			mindmaps, making it easy to visualize and explore complex information.
		</p>

		<input
			type="file"
			accept="application/pdf"
			id="upload-btn"
			on:change={handleFileUpload}
			hidden
		/>
		<label for="upload-btn" class="custom-upload-btn"
			><i class="ri-upload-line"></i>Upload File</label
		>
	</div>
</div>

<style lang="scss">
	#hero {
		align-items: center;
		display: flex;
		flex-direction: row-reverse;
		gap: 40px;
		height: 100vh;
		justify-content: space-between;
		max-width: 1536px;
		width: 100%;
		margin: 0 auto;
		padding: 0 20px;

		img {
			border-radius: var(--theme-border-radius-container);
			box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
			height: 80vh;
			object-fit: cover;
			width: 40vw;
		}

		#hero-text {
			flex: 1;
			text-align: left;

			h1 {
				font-size: 3rem;
				margin-bottom: 1rem;
			}

			p {
				font-size: 1.2rem;
				margin-bottom: 2rem;
			}

			.custom-upload-btn {
				align-items: center;
				background-color: var(--theme-title-color);
				border: none;
				border-radius: var(--theme-border-radius-container);
				color: #fff;
				cursor: pointer;
				display: inline-flex;
				font-size: 1rem;
				padding: 1rem 2rem;
				text-transform: uppercase;
				transition: background-color 0.3s ease;

				&:hover {
					background-color: var(--theme-primary-color);
				}

				i.ri-upload-line {
					font-size: 1.5rem;
					margin-right: 0.5rem;
				}
			}

			input[type='file'] {
				display: none;
			}
		}
	}
</style>
