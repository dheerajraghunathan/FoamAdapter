# SPDX-License-Identifier: Unlicense
# SPDX-FileCopyrightText: 2024 FoamAdapter authors

function(foam_adapter_example NAME)
  add_executable(${NAME} ${NAME}.cpp)
  target_compile_definitions(${NAME} INTERFACE namespaceFoam=1)
  target_link_libraries(${NAME} FoamAdapter)
  install(TARGETS ${NAME})
endfunction()

add_subdirectory(scalarAdvection)
add_subdirectory(neoIcoFoam)
add_subdirectory(heatTransfer)
