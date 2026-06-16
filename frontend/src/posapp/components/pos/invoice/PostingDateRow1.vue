<template>
	<v-sheet
		v-if="pos_profile?.posa_allow_change_posting_date"
		class="pos-header-bar px-1 py-1 mb-0"
		rounded="lg"
		elevation="0"
	>
		<v-row align="center" dense class="compact-row">
			<!-- Posting Date -->
			<v-col
				cols="12"
				:sm="showPriceList ? 4 : 5"
				:md="showPriceList ? 4 : 5"
				:lg="showPriceList ? 4 : 5"
				class="py-0 px-1"
			>
				<VueDatePicker
					ref="postingDatePicker"
					v-model="internal_posting_date_display"
					model-type="format"
					format="dd-MM-yyyy"
					auto-apply
					teleport
					:placeholder="placeholderText"
					:aria-label="placeholderText"
					class="pos-date-picker"
					@update:model-value="onUpdate"
				/>
			</v-col>

			<!-- Price List -->
			<v-col
				v-if="showPriceList"
				cols="12"
				sm="4"
				md="4"
				lg="4"
				class="py-0 px-1"
			>
				<v-select
					v-model="internal_price_list"
					:items="priceLists"
					:placeholder="priceListLabel"
					density="compact"
					variant="solo"
					color="primary"
					hide-details
					prepend-inner-icon="mdi-tag-multiple"
					class="sleek-select"
					@update:model-value="onPriceListUpdate"
				/>
			</v-col>

			<!-- Customer Balance -->
			<v-col
				v-if="showBalance"
				cols="12"
				:sm="showPriceList ? 4 : 7"
				:md="showPriceList ? 4 : 7"
				:lg="showPriceList ? 4 : 7"
				class="py-0 px-1"
			>
				<div class="balance-container">
					<span class="balance-label">{{ __("Balance") }}</span>

					<v-skeleton-loader
						v-if="balance_loading"
						type="chip"
						width="90"
						class="balance-skeleton"
					/>

					<v-tooltip
						v-else-if="isNegative"
						location="bottom"
						:text="__('Account is overdrawn')"
					>
						<template #activator="{ props: tooltipProps }">
							<v-chip
								v-bind="tooltipProps"
								size="x-small"
								color="error"
								variant="elevated"
								class="balance-chip font-weight-bold"
							>
								<v-icon start icon="mdi-alert-circle" size="12" />
								<span class="balance-amount">{{ formattedBalance }}</span>
							</v-chip>
						</template>
					</v-tooltip>

					<v-chip
						v-else
						size="x-small"
						color="success"
						variant="tonal"
						class="balance-chip font-weight-bold"
					>
						<span class="balance-amount">{{ formattedBalance }}</span>
					</v-chip>
				</div>
			</v-col>
		</v-row>
	</v-sheet>
</template>

<script setup lang="ts">
import { ref, watch, computed } from "vue";
import type { POSProfile } from "../../../types/models";

interface Props {
	pos_profile: POSProfile | Record<string, any>;
	posting_date_display?: string;
	customer_balance?: number;
	customer_balance_currency?: string;
	balance_loading?: boolean;
	formatCurrency: (val: number | undefined, currency?: string) => string;
	priceList?: string;
	priceLists?: string[];
}

const props = defineProps<Props>();

const __ = (str: string) => (window.__ ? window.__(str) : str);

const emit = defineEmits<{
	"update:posting_date_display": [val: string];
	"update:priceList": [val: string];
}>();

const internal_posting_date_display = ref(props.posting_date_display);
const internal_price_list = ref(props.priceList);
const postingDatePicker = ref<any>(null);

const showPriceList = computed(() => !!props.pos_profile?.posa_enable_price_list_dropdown);
const showBalance = computed(() => !!props.pos_profile?.posa_show_customer_balance);

const placeholderText = computed(() => __("Posting Date"));
const priceListLabel = computed(() => __("Price List"));

const isNegative = computed(() => (props.customer_balance ?? 0) < 0);
const formattedBalance = computed(() => {
	return props.formatCurrency(props.customer_balance, props.customer_balance_currency);
});

watch(() => props.posting_date_display, (val) => {
	internal_posting_date_display.value = val;
});

watch(() => props.priceList, (val) => {
	internal_price_list.value = val;
});

const onUpdate = (val: any) => {
	emit("update:posting_date_display", val);
};

const onPriceListUpdate = (val: any) => {
	emit("update:priceList", val);
};

const focusPostingDate = () => {
	const el = postingDatePicker.value?.$el || postingDatePicker.value;
	const input = el?.querySelector("input");
	if (input) {
		input.focus();
		input.select?.();
	}
};

defineExpose({ focusPostingDate });
</script>

<style scoped>
.pos-header-bar {
	background-color: var(--pos-card-bg, #ffffff);
	border: 1px solid rgba(var(--v-theme-on-surface), 0.06);
	box-shadow: none;
	min-height: 0;
}

/* Compact row */
.compact-row {
	min-height: 0;
	margin: 0;
}

/* Date Picker */
.pos-date-picker {
	width: 100%;
	min-width: 0;
}

.pos-date-picker :deep(.dp__main),
.pos-date-picker :deep(.dp__input_wrap) {
	width: 100%;
}

.pos-date-picker :deep(.dp__input) {
	width: 100%;
	min-width: 0;
	min-height: 32px;
	height: 32px;
	background-color: var(--pos-input-bg, #f5f5f5);
	color: var(--pos-text-primary, #212121);
	border-radius: 8px;
	border: 1px solid transparent;
	padding: 4px 30px 4px 9px;
	font-size: 0.82rem;
	line-height: 1.1;
	transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.pos-date-picker :deep(.dp__input:hover) {
	border-color: rgba(var(--v-theme-primary), 0.35);
}

.pos-date-picker :deep(.dp__input:focus) {
	border-color: rgb(var(--v-theme-primary));
	box-shadow: 0 0 0 1px rgba(var(--v-theme-primary), 0.14);
}

.pos-date-picker :deep(.dp__input_icon) {
	inset-inline-start: auto;
	inset-inline-end: 8px;
	color: var(--pos-text-secondary, #757575);
}

.pos-date-picker :deep(.dp__input_icon_pad) {
	padding-inline-start: 9px;
}

.pos-date-picker :deep(.dp__menu) {
	background-color: var(--pos-card-bg, #ffffff);
	color: var(--pos-text-primary, #212121);
	border-radius: 10px;
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
	z-index: 4000;
}

.pos-date-picker :deep(.dp__calendar_header_item),
.pos-date-picker :deep(.dp__cell_inner) {
	color: var(--pos-text-primary, #212121);
}

/* Price List Select */
.sleek-select :deep(.v-field) {
	border-radius: 8px;
	min-height: 32px;
	height: 32px;
	box-shadow: none;
}

.sleek-select :deep(.v-field__input) {
	min-height: 32px;
	height: 32px;
	padding-top: 2px;
	padding-bottom: 2px;
	font-size: 0.82rem;
	line-height: 1.1;
}

.sleek-select :deep(.v-field__prepend-inner) {
	padding-top: 4px;
}

.sleek-select :deep(.v-field__append-inner) {
	padding-top: 4px;
}

/* Balance */
.balance-container {
	display: flex;
	align-items: center;
	justify-content: flex-end;
	gap: 5px;
	min-width: 0;
	width: 100%;
	min-height: 32px;
	height: 32px;
	overflow: hidden;
}

.balance-label {
	font-size: 0.65rem;
	color: rgba(var(--v-theme-on-surface), 0.6);
	white-space: nowrap;
	flex: 0 1 auto;
	min-width: 0;
	overflow: hidden;
	text-overflow: ellipsis;
}

.balance-skeleton :deep(.v-skeleton-loader__chip) {
	border-radius: 14px;
	height: 24px;
}

.balance-chip {
	flex: 0 0 auto;
	font-variant-numeric: tabular-nums;
	letter-spacing: 0.01em;
	height: 24px;
	min-height: 24px;
	padding-inline: 7px;
}

.balance-amount {
	white-space: nowrap;
	font-size: 0.78rem;
	line-height: 1;
}

/* Mobile */
@media (max-width: 599px) {
	.balance-container {
		justify-content: space-between;
	}
}
</style>
