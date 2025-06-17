import QtQuick 2.15
import QtQuick.Particles 2.0
import QtMultimedia 6.8

Item {
    id: fireworks
    width: parent.width
    height: parent.height
    property bool running_p: false

    ParticleSystem {
        id: system
    }

    SoundEffect {
        id: explosionSound
        source: "./sounds/firework.wav"
        volume: 0.8
    }

    Emitter {
        id: emitter
        system: system
        emitRate: 0
        lifeSpan: 1500

        velocity: AngleDirection {
            angle: 0
            angleVariation: 360
            magnitude: 200
            magnitudeVariation: 100
        }

        acceleration: PointDirection { x: 0; y: 100 }

        width: 1
        height: 1

        Timer {
            interval: 1000 
            running: running_p
            repeat: true
            onTriggered: {
                emitter.x = Math.random() * fireworks.width
                emitter.y = Math.random() * fireworks.height / 2
                emitter.emitRate = 500
                explosionSound.play()
                Qt.createQmlObject('import QtQuick 2.0; Timer { interval: 300; repeat: false; running: true; onTriggered: emitter.emitRate = 0 }', emitter)
            }
        }
    }

    ImageParticle {
        system: system
        source: "./imgs/star.png"
        colorVariation: 1.0
        color: "yellow"
    }
}
