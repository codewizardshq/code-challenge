<template>
	<div class="home">

	</div>
</template>

<script>
import { User } from "@/store";
export default {
	name: "home",
	computed: {
		...User.mapState()
	}
};
</script>
