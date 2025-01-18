// generated from rosidl_generator_cpp/resource/rosidl_generator_cpp__visibility_control.hpp.in
// generated code does not contain a copyright notice

#ifndef AURA_MSGS__MSG__ROSIDL_GENERATOR_CPP__VISIBILITY_CONTROL_HPP_
#define AURA_MSGS__MSG__ROSIDL_GENERATOR_CPP__VISIBILITY_CONTROL_HPP_

#ifdef __cplusplus
extern "C"
{
#endif

// This logic was borrowed (then namespaced) from the examples on the gcc wiki:
//     https://gcc.gnu.org/wiki/Visibility

#if defined _WIN32 || defined __CYGWIN__
  #ifdef __GNUC__
    #define ROSIDL_GENERATOR_CPP_EXPORT_aura_msgs __attribute__ ((dllexport))
    #define ROSIDL_GENERATOR_CPP_IMPORT_aura_msgs __attribute__ ((dllimport))
  #else
    #define ROSIDL_GENERATOR_CPP_EXPORT_aura_msgs __declspec(dllexport)
    #define ROSIDL_GENERATOR_CPP_IMPORT_aura_msgs __declspec(dllimport)
  #endif
  #ifdef ROSIDL_GENERATOR_CPP_BUILDING_DLL_aura_msgs
    #define ROSIDL_GENERATOR_CPP_PUBLIC_aura_msgs ROSIDL_GENERATOR_CPP_EXPORT_aura_msgs
  #else
    #define ROSIDL_GENERATOR_CPP_PUBLIC_aura_msgs ROSIDL_GENERATOR_CPP_IMPORT_aura_msgs
  #endif
#else
  #define ROSIDL_GENERATOR_CPP_EXPORT_aura_msgs __attribute__ ((visibility("default")))
  #define ROSIDL_GENERATOR_CPP_IMPORT_aura_msgs
  #if __GNUC__ >= 4
    #define ROSIDL_GENERATOR_CPP_PUBLIC_aura_msgs __attribute__ ((visibility("default")))
  #else
    #define ROSIDL_GENERATOR_CPP_PUBLIC_aura_msgs
  #endif
#endif

#ifdef __cplusplus
}
#endif

#endif  // AURA_MSGS__MSG__ROSIDL_GENERATOR_CPP__VISIBILITY_CONTROL_HPP_
