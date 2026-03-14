<template>
	<v-row align="center" class="items px-2 py-1 compact-row" no-gutters>
		<v-col :cols="pos_profile.posa_allow_sales_order ? 9 : 12" class="pb-0 pr-1">
			<!-- Customer selection component -->
			<Customer ref="customerComponent" />
		</v-col>
		<!-- Invoice Type Selection (Only shown if sales orders are allowed) -->
		<v-col v-if="pos_profile.posa_allow_sales_order" cols="3" class="pb-0 pl-1">
			<v-select
				density="compact"
				hide-details
				variant="solo"
				color="primary"
				class="sleek-field pos-themed-input"
				:items="invoiceTypes"
				:placeholder="frappe._('Type')"
				single-line
				:model-value="modelValue"
				@update:model-value="$emit('update:modelValue', $event)"
				:disabled="modelValue == 'Return'"
			></v-select>
		</v-col>
	</v-row>
</template>

<script setup>
import { ref } from "vue";
import Customer from "../customer/Customer.vue";

defineProps({
	pos_profile: {
		type: Object,
		required: true,
		default: () => ({}),
	},
	invoiceTypes: {
		type: Array,
		default: () => ["Invoice", "Order", "Quotation"],
	},
	modelValue: {
		type: String,
		default: "Invoice",
	},
});

defineEmits(["update:modelValue"]);
const customerComponent = ref(null);

// Expose focus method for parent
const focusCustomerSearch = () => {
	if (customerComponent.value && typeof customerComponent.value.focusCustomerSearch === "function") {
		customerComponent.value.focusCustomerSearch();
	}
};

defineExpose({
	focusCustomerSearch,
});

const frappe = window.frappe;
</script>

<style scoped>
.compact-row {
	min-height: 42px;
}

:deep(.sleek-field .v-field),
:deep(.sleek-field .v-field__input) {
	min-height: 36px !important;
}
</style>
