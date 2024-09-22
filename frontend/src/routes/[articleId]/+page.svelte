<script lang="ts">
	import type { PageData } from "./$types";

	export let data: PageData;

	$: ({ article } = data);
</script>

<form action="?/updateArticle" method="post">
	<h3>Editing: {article.title}</h3>

	<label for="title">Title:</label>
	<input type="text" id="title" name="title" value={article.title}>

	<label for="content">Content:</label>
	<textarea id="content" name="content" rows="5" value={article.content}></textarea>

	<button type="submit">Update Article</button>
</form>
