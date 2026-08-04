//
// Created by jordan on 6/8/26.
//
#include "traffic_light.h"
/**
 *
 * @signal{light_changed(TrafficLightType new_state)| This signal is emitted when the state of the Traffic Light changes.
 *
 * Test to make sure this second paragraph is read as part of the signal description}
 * @signal{light_changing(TrafficLightType old_state,TrafficLightType new_state)| this signal is emitted when the light is about to change.
 * The signal parameter indicate the current state and what the new state will be}
 */
void TrafficLight::_bind_methods()
{
    ClassDB::bind_method(D_METHOD("set_go_texture","texture"), &TrafficLight::set_go_texture);
	ClassDB::bind_method(D_METHOD("get_go_texture"), &TrafficLight::get_go_texture);
    ClassDB::bind_method(D_METHOD("set_caution_texture","texture"), &TrafficLight::set_caution_texture);
    ClassDB::bind_method(D_METHOD("get_caution_texture"), &TrafficLight::get_caution_texture);
    ClassDB::bind_method(D_METHOD("set_stop_texture","texture"), &TrafficLight::set_stop_texture);
    ClassDB::bind_method(D_METHOD("get_stop_texture"), &TrafficLight::get_stop_texture);
    ClassDB::bind_method(D_METHOD("set_light_type","light_type"), &TrafficLight::set_light_type);
    ClassDB::bind_method(D_METHOD("get_light_type"), &TrafficLight::get_light_type);
	ClassDB::bind_method(D_METHOD("show_next_light"), &TrafficLight::show_next_light);
	// ClassDB::bind_method(D_METHOD("commented_method"), &TrafficLight::get_light_type);

	ADD_PROPERTY
    (
        PropertyInfo(Variant::OBJECT,"go_texture",PROPERTY_HINT_RESOURCE_TYPE,"Texture2D"),
        "set_go_texture","get_go_texture"
        );
    ADD_PROPERTY
    (
        PropertyInfo(Variant::OBJECT,"caution_texture",PROPERTY_HINT_RESOURCE_TYPE,"Texture2D"),
        "set_caution_texture","get_caution_texture"
        );
    ADD_PROPERTY
    (
        PropertyInfo(Variant::OBJECT,"stop_texture",PROPERTY_HINT_RESOURCE_TYPE,"Texture2D"),
        "set_stop_texture","get_stop_texture"
        );

    ADD_PROPERTY
    (
        PropertyInfo(Variant::INT,"light_type",PROPERTY_HINT_ENUM,"Go:5,Caution:50,Stop:500"),
        "set_light_type","get_light_type"
        );

	/*ADD_PROPERTY
	(
		PropertyInfo(Variant::OBJECT,"commented_property",PROPERTY_HINT_RESOURCE_TYPE,"Texture2D"),
		"set_comment","get_comment"
		);*/


    BIND_ENUM_CONSTANT(TRAFFIC_LIGHT_GO)
	BIND_ENUM_CONSTANT(TRAFFIC_LIGHT_CAUTION)
	BIND_ENUM_CONSTANT(TRAFFIC_LIGHT_STOP)

	//  ADD_SIGNAL(MethodInfo("light_signal_comment",PropertyInfo(Variant::INT,"light_type",PROPERTY_HINT_ENUM,"Go,Caution,Stop","TrafficLightType")));
	ADD_SIGNAL(MethodInfo(
	   "light_changed",
	   PropertyInfo(
		   Variant::INT,                                       // 1. Data Type
		   "light_type",                                       // 2. Argument Name
		   PROPERTY_HINT_NONE,                                 // 3. Hint
		   "",                                                 // 4. Hint String (Empty)
		   PROPERTY_USAGE_DEFAULT | PROPERTY_USAGE_CLASS_IS_ENUM, // 5. Enforce class enum usage
		   "TrafficLightType"                           // 6. Explicit Object Target String
	   )
   ));

	ADD_SIGNAL(MethodInfo("light_changing",
		PropertyInfo(Variant::INT,"current_light_type",PROPERTY_HINT_NONE,"",PROPERTY_USAGE_DEFAULT|PROPERTY_USAGE_CLASS_IS_ENUM,"TrafficLightType"),
		PropertyInfo(Variant::INT,"new_light_type",PROPERTY_HINT_NONE,"",PROPERTY_USAGE_DEFAULT|PROPERTY_USAGE_CLASS_IS_ENUM,"TrafficLightType")));

	GDVIRTUAL_BIND(_get_next_light,"previous_light")
}
