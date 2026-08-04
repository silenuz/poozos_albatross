//
// Created by jordan on 4/1/26.
//

#include "traffic_light.h"
//
// Created by jordan on 4/1/26.
//

#include "traffic_light.h"

void TrafficLight::_notification(int p_what)
{
    switch (p_what)
    {
       case NOTIFICATION_READY:
            set_light_type(light_type);
            break;
    }
}

void TrafficLight::show_next_light()
{
	TrafficLightType next_light_type;
	if (GDVIRTUAL_CALL(_get_next_light,light_type,next_light_type)) {
		set_light_type(next_light_type);
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

