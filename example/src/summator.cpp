/*
 * This source code was "borrowed" from the Godot documentation.
 * © Copyright 2014-2026, Juan Linietsky, Ariel Manzur and the Godot community (CC-BY 3.0)
 * and the original can be found at https://docs.godotengine.org/en/4.4/contributing/development/core_and_modules/custom_modules_in_cpp.html#creating-a-new-module
 *
 */
#include "summator.h"
#include <godot_cpp/core/class_db.hpp>

void Summator::_bind_methods() {
	ClassDB::bind_method(D_METHOD("add", "value"), &Summator::add);
	ClassDB::bind_method(D_METHOD("reset"), &Summator::reset);
	ClassDB::bind_method(D_METHOD("get_total"), &Summator::get_total);

	ADD_SIGNAL(MethodInfo("sum_changed", PropertyInfo(Variant::INT, "sum")));
	ADD_SIGNAL(MethodInfo("sum_reset"));

	// Register the constant with ClassDB
	ClassDB::bind_integer_constant(
			"Summator", // Class name in Godot
			"", // enumerator group
			"SUM_REQUIRED", // Name visible in GDScript
			MINMUM_REQUIRED_AMOUNT // The actual value
	);
	ClassDB::bind_integer_constant("Summator","","SUM_OKAY",DOING_OKAY_AMOUNT);
	ClassDB::bind_integer_constant("Summator","","SUM_GOOD",DOING_NOTHING_AMOUNT);
}

void Summator::add(int p_value) {
	sum += p_value;
	emit_signal("sum_changed", sum);
}
void Summator::reset() {
	sum = 0;
	emit_signal("sum_changed", sum);
	emit_signal("sum_reset");
}
int Summator::get_total() const {
	return sum;
}

Summator::Summator() {
	sum = 0;
}