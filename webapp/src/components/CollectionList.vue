<template>
  <span v-for="collection in collections" :key="collection.collection_id">
    <FormattedCollectionName
      :collection_id="collection.collection_id"
      enableClick
      enableModifiedClick
    />
  </span>
</template>

<script>
import FormattedCollectionName from "@/components/FormattedCollectionName.vue";

export default {
  data() {
    return {};
  },
  props: {
    collections: {
      type: Array,
    },
  },
  components: {
    FormattedCollectionName,
  },
};
</script>
