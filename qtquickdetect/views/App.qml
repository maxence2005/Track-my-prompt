// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only

import QtQuick

Window {
    minimumWidth: 1000
    minimumHeight: 600
    width: mainScreen.width
    height: mainScreen.height

    visible: true
    title: "TrackMyPrompts"

    AppView {
        id: mainScreen
    }

}

