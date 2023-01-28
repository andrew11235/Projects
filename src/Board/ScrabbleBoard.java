package Board;

import BoardTiles.DoubleLetter.DoubleLetter;
import BoardTiles.DoubleWord.DoubleWord;
import BoardTiles.StartTile.StartTile;
import BoardTiles.TripleLetter.TripleLetter;
import BoardTiles.TripleWord.TripleWord;
import info.gridworld.actor.ActorWorld;
import info.gridworld.grid.BoundedGrid;
import info.gridworld.grid.Location;


public class ScrabbleBoard extends ActorWorld {
    /**
     * ScrabbleBoard constructor creates a new ActorWorld which mimics the setup of a Scrabble board
     */
    public ScrabbleBoard() {
        super(new BoundedGrid<>(15, 15));
        this.add(new Location(0, 3), new DoubleLetter());
        this.add(new Location(0, 11), new DoubleLetter());
        this.add(new Location(2, 6), new DoubleLetter());
        this.add(new Location(2, 8), new DoubleLetter());
        this.add(new Location(3, 0), new DoubleLetter());
        this.add(new Location(3, 7), new DoubleLetter());
        this.add(new Location(3, 14), new DoubleLetter());
        this.add(new Location(6, 2), new DoubleLetter());
        this.add(new Location(6, 6), new DoubleLetter());
        this.add(new Location(6, 8), new DoubleLetter());
        this.add(new Location(6, 12), new DoubleLetter());
        this.add(new Location(7, 3), new DoubleLetter());
        this.add(new Location(7, 11), new DoubleLetter());
        this.add(new Location(8, 2), new DoubleLetter());
        this.add(new Location(8, 6), new DoubleLetter());
        this.add(new Location(8, 8), new DoubleLetter());
        this.add(new Location(8, 12), new DoubleLetter());
        this.add(new Location(11, 0), new DoubleLetter());
        this.add(new Location(11, 7), new DoubleLetter());
        this.add(new Location(11, 14), new DoubleLetter());
        this.add(new Location(12, 6), new DoubleLetter());
        this.add(new Location(12, 8), new DoubleLetter());
        this.add(new Location(14, 3), new DoubleLetter());
        this.add(new Location(14, 11), new DoubleLetter());

        this.add(new Location(1, 5), new TripleLetter());
        this.add(new Location(1, 9), new TripleLetter());
        this.add(new Location(5, 1), new TripleLetter());
        this.add(new Location(5, 5), new TripleLetter());
        this.add(new Location(5, 9), new TripleLetter());
        this.add(new Location(5, 13), new TripleLetter());
        this.add(new Location(9, 1), new TripleLetter());
        this.add(new Location(9, 5), new TripleLetter());
        this.add(new Location(9, 9), new TripleLetter());
        this.add(new Location(9, 13), new TripleLetter());
        this.add(new Location(13, 5), new TripleLetter());
        this.add(new Location(13, 9), new TripleLetter());

        this.add(new Location(1, 1), new DoubleWord());
        this.add(new Location(2, 2), new DoubleWord());
        this.add(new Location(3, 3), new DoubleWord());
        this.add(new Location(4, 4), new DoubleWord());
        this.add(new Location(10, 10), new DoubleWord());
        this.add(new Location(11, 11), new DoubleWord());
        this.add(new Location(12, 12), new DoubleWord());
        this.add(new Location(13, 13), new DoubleWord());
        this.add(new Location(13, 1), new DoubleWord());
        this.add(new Location(12, 2), new DoubleWord());
        this.add(new Location(11, 3), new DoubleWord());
        this.add(new Location(10, 4), new DoubleWord());
        this.add(new Location(4, 10), new DoubleWord());
        this.add(new Location(3, 11), new DoubleWord());
        this.add(new Location(2, 12), new DoubleWord());
        this.add(new Location(1, 13), new DoubleWord());

        this.add(new Location(0, 0), new TripleWord());
        this.add(new Location(0, 7), new TripleWord());
        this.add(new Location(0, 14), new TripleWord());
        this.add(new Location(7, 0), new TripleWord());
        this.add(new Location(7, 14), new TripleWord());
        this.add(new Location(14, 0), new TripleWord());
        this.add(new Location(14, 7), new TripleWord());
        this.add(new Location(14, 14), new TripleWord());

        this.add(new Location(7, 7), new StartTile());
    }
}
