//
// Created by jordan on 4/1/26.
//

#include "traffic_light.h"
//
// Created by jordan on 4/1/26.
//

#include "traffic_light.h"

/**
 *
 * @signal{light_changed(TrafficLightType new_state)| This signal is emitted when the state of the Traffic Light changes.}
 * @signal{light_changing(TrafficLightType old_state,TrafficLightType new_state)| this signal is emitted when the light is about to change.
 * The signal parameter indicate the current state and what the new state will be}
 */
void TrafficLight::_bind_methods()
{
    ClassDB::bind_method(D_METHOD("set_go_texture","texture"), &TrafficLight::set_go_texture);    ClassDB::bind_method(D_METHOD("get_go_texture"), &TrafficLight::get_go_texture);
    ClassDB::bind_method(D_METHOD("set_caution_texture","texture"), &TrafficLight::set_caution_texture);
    ClassDB::bind_method(D_METHOD("get_caution_texture"), &TrafficLight::get_caution_texture);
    ClassDB::bind_method(D_METHOD("set_stop_texture","texture"), &TrafficLight::set_stop_texture);
    ClassDB::bind_method(D_METHOD("get_stop_texture"), &TrafficLight::get_stop_texture);
    ClassDB::bind_method(D_METHOD("set_light_type","light_type"), &TrafficLight::set_light_type);
    ClassDB::bind_method(D_METHOD("get_light_type"), &TrafficLight::get_light_type);

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
        PropertyInfo(Variant::INT,"light_type",PROPERTY_HINT_ENUM,"Go,Caution,Stop"),
        "set_light_type","get_light_type"
        );

    BIND_ENUM_CONSTANT(TRAFFIC_LIGHT_GO)
	BIND_ENUM_CONSTANT(TRAFFIC_LIGHT_CAUTION)
	BIND_ENUM_CONSTANT(TRAFFIC_LIGHT_STOP)


	//ADD_SIGNAL(MethodInfo("light_changed",PropertyInfo(Variant::INT,"light_type",PROPERTY_HINT_ENUM,"Go,Caution,Stop","TrafficLightType")));
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
		PropertyInfo(Variant::INT,"current_light_type",PROPERTY_HINT_NONE,"",PROPERTY_USAGE_DEFAULT|PROPERTY_USAGE_CLASS_IS_ENUM,"TarfficLightType"),
		PropertyInfo(Variant::INT,"new_light_type",PROPERTY_HINT_NONE,"",PROPERTY_USAGE_DEFAULT|PROPERTY_USAGE_CLASS_IS_ENUM,"TrafficLightType")));
}

void TrafficLight::_notification(int p_what)
{
    switch (p_what)
    {
       NOTIFICATION_READY:
            set_light_type(light_type);
            break;
    }
}

TrafficLightType TrafficLight::get_light_type() const
{
    return light_type;
}

void TrafficLight::set_light_type(TrafficLightType p_light_type)
{
    light_type = p_light_type;

    switch (light_type)
    {
        case TrafficLightType::TRAFFIC_LIGHT_GO:
            texture_rect->set_texture(go_texture);
            break;
        case TrafficLightType::TRAFFIC_LIGHT_STOP:
            texture_rect->set_texture(stop_texture);
            break;
        case TrafficLightType::TRAFFIC_LIGHT_CAUTION:
            texture_rect->set_texture(caution_texture);
            break;
        default:
            texture_rect->set_texture(go_texture);
    }
}

Ref<Texture2D> TrafficLight::get_go_texture() const
{
    return go_texture;
}

Ref<Texture2D> TrafficLight::get_stop_texture() const
{
    return stop_texture;
}

Ref<Texture2D> TrafficLight::get_caution_texture() const
{
    return caution_texture;
}

void TrafficLight::set_caution_texture(const Ref<Texture2D> &p_texture)
{
    caution_texture = p_texture;
}

void TrafficLight::set_go_texture(const Ref<Texture2D> &p_texture)
{
    go_texture = p_texture;
}

void TrafficLight::set_stop_texture(const Ref<Texture2D> &p_texture)
{
    stop_texture = p_texture;
}

TrafficLight::TrafficLight()
{
    texture_rect = memnew(TextureRect);
    add_child(texture_rect);
    texture_rect->set_anchors_preset(LayoutPreset::PRESET_FULL_RECT);
    light_type = TrafficLightType::TRAFFIC_LIGHT_GO;

}

