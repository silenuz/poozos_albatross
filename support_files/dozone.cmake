find_package(Doxygen)

if(DOXYGEN_FOUND)
    ############################################################################################
    ###                                     Configure                                        ###
    ############################################################################################

    # set project settings
    set(DOXYGEN_PROJECT_NAME ${LIBNAME})
    set(DOXYGEN_PROJECT_NUMBER ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR})
    option(GENERATE_BUILD_PROFILE "Generate a build_profile.json file from the doxygen XML" NO)
    # Optional: Set the path to your logo file
    #set(DOXYGEN_PROJECT_LOGO "${CMAKE_CURRENT_SOURCE_DIR}/logo.png")
    # Optional: Set a favicon (requires Doxygen 1.10.0+)
    #set(DOXYGEN_PROJECT_ICON "${CMAKE_CURRENT_SOURCE_DIR}/icon.ico")

    # Output format settings
    set(DOXYGEN_GENERATE_HTML YES)
    set(DOXYGEN_GENERATE_LATEX NO)
    set(DOXYGEN_GENERATE_MAN NO)
    set(DOXYGEN_GENERATE_RTF NO)

    # generate xml so it can be later converted to Godot class documentation
    set(DOXYGEN_GENERATE_XML YES)

    # help save repetitive typing
    Set(GODOT_LINK_START "<godotonly position=\\\"open\\\" content=\\\"[")
    set(GODOT_LINK_CLOSE "<godotonly position=\\\"close\\\" content=\\\"]\\\"></godotonly>")
    set(GODOT_OPERATOR_LINK_CLOSE "<godotonly position=\\\"close\\\" content=\\\" *]\\\"></godotonly>")

    # create an alias so we can use @glnk{} or \glnk{} in comments to create output for Godot documentation only
    # so that doxygen xml output remains compatible with Breathe.
    set(DOXYGEN_ALIASES
            ## define aliases for various godot documentation only links see https://docs.godotengine.org/en/stable/engine_details/class_reference/index.html#linking
            "glnk{1}=\"\\xmlonly${GODOT_LINK_START}\\\"></godotonly>\\endxmlonly\\1\\xmlonly${GODOT_LINK_CLOSE}\\endxmlonly\""
            "gdcon{2}=\"\\xmlonly${GODOT_LINK_START}constant \\1.\\\"></godotonly>\\endxmlonly\\2\\xmlonly${GODOT_LINK_CLOSE}\\endxmlonly\""
            "gdcon{2}=\"\\xmlonly${GODOT_LINK_START}constant \\1.\\\"></godotonly>\\endxmlonly\\2\\xmlonly${GODOT_LINK_CLOSE}\\endxmlonly\""
            "gdenu{2}=\"\\xmlonly${GODOT_LINK_START}enum \\1.\\\"></godotonly>\\endxmlonly\\2\\xmlonly${GODOT_LINK_CLOSE}\\endxmlonly\""
            "gdmem{2}=\"\\xmlonly${GODOT_LINK_START}member \\1.\\\"></godotonly>\\endxmlonly\\2\\xmlonly${GODOT_LINK_CLOSE}\\endxmlonly\""
            "gdmet{2}=\"\\xmlonly${GODOT_LINK_START}method \\1.\\\"></godotonly>\\endxmlonly\\2\\xmlonly${GODOT_LINK_CLOSE}\\endxmlonly\""
            "gdnew{2}=\"\\xmlonly${GODOT_LINK_START}constructor \\1.\\\"></godotonly>\\endxmlonly\\2\\xmlonly${GODOT_LINK_CLOSE}\\endxmlonly\""
            "gdope{2}=\"\\xmlonly${GODOT_LINK_START}operator \\1.\\\"></godotonly>\\endxmlonly\\2\\xmlonly${GODOT_OPERATOR_LINK_CLOSE}\\endxmlonly\""
            "gdsig{2}=\"\\xmlonly${GODOT_LINK_START}signal \\1.\\\"></godotonly>\\endxmlonly\\2\\xmlonly${GODOT_LINK_CLOSE}\\endxmlonly\""
            "gdthe{2}=\"\\xmlonly${GODOT_LINK_START}theme_item \\1.\\\"></godotonly>\\endxmlonly\\2\\xmlonly${GODOT_LINK_CLOSE}\\endxmlonly\""
            "gdpar{1}=\"\\xmlonly${GODOT_LINK_START}param\\\"></godotonly>\\endxmlonly\\1\\xmlonly${GODOT_LINK_CLOSE}\\endxmlonly\""
            # signal alias uses | pipes as a parameter seperator so that commas don't have to be escaped
            "signal{2|}=\"\\xrefitem signal \\\"Signal\\\" \\\"Signals\\\"\\xmlonly<godotonly reference=\\\"signal\\\" name=\\\"\\1\\\"/>\\endxmlonly@parblock<b>\\1:</b> ^^^^^^ \\2@endparblock\""
    )

   set(DOXYGEN_VERBATIM_VARS DOXYGEN_ALIASES)

    # set directory to create the docs in
    set(DOXYGEN_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/docs)

    # set the project read me file as the content of the main index page of
    # the documentation
    set(DOXYGEN_USE_MDFILE_AS_MAINPAGE "${CMAKE_CURRENT_SOURCE_DIR}/README.md")

    # exclude register_types, and if still present the example class from the
    # godot cpp template
    set(DOXYGEN_EXCLUDE_PATTERNS
            "register_types.h"
            "register_types.cpp"
            "example_class.h"
            "example_class.cpp"
    )

    #todo: Fix so that doxygen input folders are retrieved based on library target source directories
    #[[ add_custom_command(
         TARGET doc_doxygen
         POST_BUILD
         COMMAND ${CMAKE_COMMAND} -E echo " INTERFACES:$<TARGET_PROPERTY:${LIBNAME},INTERFACE_INCLUDE_DIRECTORIES>"
 )]]

    # configure input directories, this tells doxygen where to look for content
    # to document
    set(DOX_INPUT
            "${CMAKE_CURRENT_SOURCE_DIR}/src"
    )

    ############################################################################################
    ###                                    Build                                             ###
    ############################################################################################

    # Generate the Doxyfile and documentation when the target
    # is doc_doxygen
    doxygen_add_docs(doc_doxygen
            ${DOX_INPUT}
            ${CMAKE_CURRENT_SOURCE_DIR}/README.md
            COMMENT "Generating Doxygen docs"
    )


    # call python script to convert doxygen xml to Godot class documentation xml
    add_custom_command(
            TARGET doc_doxygen
            POST_BUILD
            COMMAND Python3::Interpreter "${CMAKE_CURRENT_SOURCE_DIR}/cmake/doxy_to_godot.py"
            "${DOXYGEN_OUTPUT_DIRECTORY}/xml"
            "${CMAKE_CURRENT_SOURCE_DIR}/doc_classes"
            COMMENT "Generating Godot class documentation"
            VERBATIM
    )

    if(GENERATE_BUILD_PROFILE)
        # call python script to generate a build_profile json file from the doxygen xml
        add_custom_command(
                TARGET doc_doxygen
                POST_BUILD
                COMMAND Python3::Interpreter "${CMAKE_CURRENT_SOURCE_DIR}/cmake/doxy_build_profile.py"
                "${DOXYGEN_OUTPUT_DIRECTORY}/xml"
                "${CMAKE_CURRENT_SOURCE_DIR}/doc_classes"
                COMMENT "Generating Build Profile"
                VERBATIM
        )
    endif ()
 else()
   message(STATUS "Doxygen Not Found")
endif()
