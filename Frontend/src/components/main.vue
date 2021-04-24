<template>
  <img :src="imgUrl" alt="Pulpit rock" width="1450" height="800" align="center">
</template>

<script>
  export default{
  data(){
    return {
      imgUrl:require("../../static/images/preview.jpeg")
    }
  }
}
</script>

<style scoped>
</style>
