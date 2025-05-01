// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 FoamAdapter authors

#include <cstddef>
#define CATCH_CONFIG_RUNNER // Define this before including catch.hpp to create
                            // a custom main
#include <unordered_set>
#include <set>

#include "common.hpp"

#include "gaussConvectionScheme.H"


namespace fvcc = NeoN::finiteVolume::cellCentred;
namespace dsl = NeoN::dsl;

extern Foam::Time* timePtr;    // A single time object
extern Foam::argList* argsPtr; // Some forks want argList access at createMesh.H
extern Foam::fvMesh* meshPtr;  // A single mesh object


TEST_CASE("sparsityPattern")
{
    Foam::Time& runTime = *timePtr;
    Foam::argList& args = *argsPtr;

    auto [execName, exec] = GENERATE(allAvailableExecutor());

    auto meshPtr = FoamAdapter::createMesh(exec, runTime);
    FoamAdapter::MeshAdapter& mesh = *meshPtr;
    auto& nfMesh = mesh.nfMesh();

    SECTION("sparsityPattern_" + execName)
    {
        fvcc::SparsityPattern pattern(nfMesh);
        const auto colIdxs = pattern.colIdxs().view();
        const auto rowPtrs = pattern.rowOffs().view();

        REQUIRE(colIdxs.size() == mesh.nCells() + 2 * mesh.nInternalFaces());
        REQUIRE(rowPtrs.size() == mesh.nCells() + 1);

        for (auto celli = 0; celli < mesh.nCells(); celli++)
        {
            std::set<Foam::label> stencilCells;
            stencilCells.insert(celli);

            // get cells connected to celli
            for (auto neiCelli : mesh.cellCells()[celli])
            {
                stencilCells.insert(neiCelli);
            }

            // test if columns in corresponding rows are in stencil cells set
            for (auto i = rowPtrs[celli]; i < rowPtrs[celli + 1]; i++)
            {
                auto colIdx = colIdxs[i];
                REQUIRE(stencilCells.contains(colIdx));
            }
        }
    }
}
