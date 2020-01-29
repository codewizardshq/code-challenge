<template>
	<div class="quiz-scroll" ref="scroll">
		<div class="scroll-graphic"></div>
		<div class="scroll-head">
			<div class="scroll-title">
				<slot name="title"></slot>
			</div>
		</div>
		<div class="scroll-body" ref="body">
			<slot name="default"></slot>
		</div>
	</div>
</template>

<script>
export default {
	name: "quizScroll"
};
</script>
