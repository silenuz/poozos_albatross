/*
 * This source code was "borrowed" from the Godot documentation.
 * © Copyright 2014-2026, Juan Linietsky, Ariel Manzur and the Godot community (CC-BY 3.0)
 *
 */

#ifndef GODOT_CPP_TEMPLATE_TRAFFIC_LIGHT_H
#define GODOT_CPP_TEMPLATE_TRAFFIC_LIGHT_H
#pragma once

#include <godot_cpp/classes/control.hpp>
#include <godot_cpp/classes/texture2d.hpp>
#include <godot_cpp/classes/texture_rect.hpp>

using namespace godot;

/**
 * TrafficLightType enumerator
 * the traffic light enumerator is used to track the current state of the light (Go,Caution,Stop)
 */
enum TrafficLightType {
	TRAFFIC_LIGHT_GO , /**< Represents a light indicating Go*/
	TRAFFIC_LIGHT_CAUTION = 500, /**< Represents a light indicating Caution*/
	TRAFFIC_LIGHT_STOP /**< Represents a light indicating Stop*/
};

/**
 * @class TrafficLight
 * @brief A classic code example from _Godotcon 2024_
 *
 *  ~~stolen~~ **borrowed** from _Godotcon 2024_
 *
 * The class <u>must inherit</u> from a Godot built in class (like @glnk{Object}, @glnk{Node}, @glnk{Sprite2D}, or @glnk{Resource}).
 * Godot does not support multiple inheritance for GDExtension classes.
 *
 */
class TrafficLight : public godot::Control {
	GDCLASS(TrafficLight, Control);

	TextureRect *texture_rect;

	Ref<Texture2D> go_texture; /**< The @glnk{Texture2D} used for displaying the Go state */
	Ref<Texture2D> stop_texture; /**< The @glnk{Texture2D} used for displaying the Stop state */
	Ref<Texture2D> caution_texture; /**< The @glnk{Texture2D} used for displaying the Caution state */
	TrafficLightType light_type; /**< The current,state of the traffic light (Go, Caution, Stop ), see @gdenu{TrafficLight,TrafficLightType} */

protected:
	/**
	 * You must declare a protected static void `_bind_methods()` function in your class header.
	 */
	static void _bind_methods();
	/**
	 * Primary method used to handle engine-level callbacks, such as an object's life cycle events or node status changes
	 * @param p_what the notification value from the Godot engine some common ones are READY,PROCESS,ENTER_TREE, and EXIT_TREE
	 */
	void _notification(int p_what);

public:
	/**
	 * constructor
	 */
	TrafficLight();

	/**
	 * Sets the @glnk{Texture2D} to be used when the light is in a (Go state
	 * @param p_texture the texture to be used
	 */
	void set_go_texture(const Ref<Texture2D> &p_texture);

	/**
	 * Gets the @glnk{Texture2D} that acts as the texture for the Go state
	 * @return the current @glnk{Texture2D} being used to represent Go
	 */
	Ref<Texture2D> get_go_texture() const;

	/**
	 * Sets the @glnk{Texture2D} to be used when the light is in a Caution state
	 * @param p_texture the texture to be used
	 */
	void set_caution_texture(const Ref<Texture2D> &p_texture);

	/**
	 * Gets the @glnk{Texture2D} that acts as the texture for the Caution state
	 * @return the current Texture2D being used to represent Caution
	 */
	Ref<Texture2D> get_caution_texture() const;

	/**
	 * Sets the @glnk{Texture2D} to be used when the light is in a Stop state
	 * @param p_texture the texture to be used
	 */
	void set_stop_texture(const Ref<Texture2D> &p_texture);

	/**
	 * Gets the @glnk{Texture2D} that acts as the texture for the Stop state
	 * @return the current Texture2D being used to represent Stop
	 */
	Ref<Texture2D> get_stop_texture() const;

	/**
	 * Sets the current state of the light to a value from @gdenu{TrafficLight,TrafficLightType}
	 * @param p_light_type the traffic light type enumerator
	 */
	void set_light_type(TrafficLightType p_light_type);

	/**
	 * Gets the current state of the traffic light, a value from @gdenu{TrafficLight,TrafficLightType}
	 * @return the traffic light type enumerator for the current light state(go,caution,stop)
	 */
	TrafficLightType get_light_type() const;
};

VARIANT_ENUM_CAST(TrafficLightType);
#endif //GODOT_CPP_TEMPLATE_TRAFFIC_LIGHT_H