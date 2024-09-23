<header class="bg-body-color fixed left-0 shadow-[0_2px_16px_hsla(230,75%,32%,0.15)] top-0 w-full z-fixed" id="header">
	<nav class="flex h-header items-center justify-between max-w-[1120px] me-6 ms-6">
		 <a href="/" class="duration-[0.4s] font-semi-bold hover:text-first-color text-title-color transition-[color]">TopicNet</a>

		 <div class="lg:mx-auto max-lg:bg-body-color max-lg:duration-[0.4s] max-lg:fixed max-lg:left-0 max-lg:pb-16 max-lg:pt-16 max-lg:shadow-[0_8px_16px_hsla(230,75%,32%,0.15)] max-lg:top-[-100%] max-lg:transition-[top] max-lg:w-full" id="nav-menu">
				<ul class="flex flex-col gap-y-10 lg:flex-row lg:gap-x-12 text-center">
					 <li>
							<!-- svelte-ignore a11y-invalid-attribute -->
							<a href="#" class="duration-[0.4s] font-semi-bold hover:text-first-color text-title-color transition-[color]">Home</a>
					 </li>

					 <li>
							<!-- svelte-ignore a11y-invalid-attribute -->
							<a href="#" class="duration-[0.4s] font-semi-bold hover:text-first-color text-title-color transition-[color]">About Us</a>
					 </li>

					 <!-- svelte-ignore a11y-invalid-attribute -->
					 <li>
							<a href="#" class="duration-[0.4s] font-semi-bold hover:text-first-color text-title-color transition-[color]">Services</a>
					 </li>

					 <li>
							<!-- svelte-ignore a11y-invalid-attribute -->
							<a href="#" class="duration-[0.4s] font-semi-bold hover:text-first-color text-title-color transition-[color]">Featured</a>
					 </li>

					 <li>
							<!-- svelte-ignore a11y-invalid-attribute -->
							<a href="#" class="duration-[0.4s] font-semi-bold hover:text-first-color text-title-color transition-[color]">Contact Us</a>
					 </li>
				</ul>

				<!-- Close button -->
				<div class="absolute cursor-pointer duration-[0.4s] lg:hidden right-6 text-title-color text-xl top-5 transition-[color]" id="nav-close">
					 <i class="ri-close-line"></i>
				</div>
		 </div>

		 <div class="flex gap-x-4 items-center">
				<!-- Search button -->
				<i class="cursor-pointer duration-[0.4s] hover:text-first-color ri-search-line text-title-color text-xl transition-[color]" id="search-btn"></i>

				<!-- Login button -->
				<i class="cursor-pointer duration-[0.4s] hover:text-first-color ri-user-line text-title-color text-xl transition-[color]" id="login-btn"></i>

				<!-- Toggle button -->
				<div class="cursor-pointer duration-[0.4s] hover:text-first-color text-title-color text-xl transition-[color]" id="nav-toggle">
					 <i class="ri-menu-line"></i>
				</div>
		 </div>
	</nav>
</header>
