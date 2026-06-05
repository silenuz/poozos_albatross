//
// Created by jordan on 5/10/26.
//

/*
 * This source code was "borrowed" from the Godot documentation.
 * © Copyright 2014-2026, Juan Linietsky, Ariel Manzur and the Godot community (CC-BY 3.0)
 * and the original can be found at https://docs.godotengine.org/en/4.4/contributing/development/core_and_modules/custom_modules_in_cpp.html#creating-a-new-module
 *
*/
#pragma once
#include <godot_cpp/classes/object.hpp>

using namespace godot;

/**
 * @class Summator
 * @brief A _classic_ code example for a **GDExtension**
 *
 * The class must inherit from a Godot built in class (like @glnk{Object}, @glnk{Node}, @glnk{Sprite2D}, or @glnk{Resource}).
 * Godot does not support multiple inheritance for GDExtension classes.
 *  Why the #@@# does the editor documentation allow csharp code blocks if it never displays them?
 *
 *  Example Usage:
 *  \code{.csharp}
 *	GodotObject sum = ClassDB.Instantiate("Summator").As<GodotObject>();
 *	sum.Call("add",5);
 *	sum.Call("add",7);
 *	int total = sum.Call("get_total").As<int>();
 *	// prints 12
 *	GD.Print(total);
 *  \endcode
 *	\code{.gdscript}
 *  var sum = Summator.new()
 *	sum.add(5)
 *	sum.add(7)
 *	var total = sum.get_total()
 *	# prints 12
 *	print(total)
 * \endcode
 *
 * @signal{sum_changed(int: sum)|
 * This **signal**, is _emitted_ when the sum changes whether
 * after adding a new integer or when resetting the total back to zero.
 *
 * @note “You're on Earth. There's no cure for that.” ― Samuel Beckett  }
 *
 * @signal{sum_reset()| This signal is emitted when the total is reset to zero
 * @note Gogo: 'We always find something, eh Didi, to give us the impression we exist?"
 * @warning I'm making this up as I go along }
 *
 * @signal{doesnt_exist|This is just a plain description, no warning or note for parser testing.  This signal
 * doesn't actually exist, so don't try to use it.  This should only output to html as the signal is not actually registered
 * with ClassDB.}
 *
 * Check Status Example:
 *	\code{.gdscript}
 * if total >= sum.SUM_GOOD:
 *	   print("Life is good")
 * elif total >= sum.SUM_OKAY:
 *	   print("Could be doing better")
 * elif total >= sum.SUM_REQUIRED:
 *	   print("At least you making rent")
 * else:
 *	   print("Your broke")
 * \endcode
 */
class Summator : public Object
{
	// GDCLASS macro placed at beginning of class body
	GDCLASS(Summator,Object);

	// current total
	int sum;

protected:
	/**
	 * You must declare a protected static void _bind_methods() function in your class header.
	 */
	static void _bind_methods();

public:

	static constexpr int MINMUM_REQUIRED_AMOUNT = 50; /**<The minimum total that is required to meet expenses */
	/** Meeting expenses with a little extra */
	static const int DOING_OKAY_AMOUNT = 100;
	/** Things are going good, well into the black */
	static const int DOING_NOTHING_AMOUNT = 200;

	/**
	 * @brief adds the passed value to the current total
	 *
	 * This function simply adds the integer value of the argument to the current total
	 *
	 * @param p_value integer value to be added to the current total
	 * */
	void add(int p_value);

	/**
	 * @brief resets the total to zero
	 *
	 * resets the current total to zero
	 */
	void reset();

	/**
	 * @brief returns the current total
	 *
	 * This function returns the current total, which is the sum of all the integers
	 * the summator added together.
	 *
	 * @return the sum of all the integers that were added together
	 */
	int get_total() const;

	/**
	 * @brief constructor
	 *
	 *  Create a new instance of the Summator class
	 */
	Summator();
};

