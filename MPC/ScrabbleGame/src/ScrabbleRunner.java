/*
Scrabble Game

Andrew Wang 2022
Version 1.0.0
 */

import Board.ScrabbleBoard;

import BoardTiles.DoubleLetter.DoubleLetter;
import BoardTiles.DoubleWord.DoubleWord;
import BoardTiles.StartTile.StartTile;
import BoardTiles.TripleLetter.TripleLetter;
import BoardTiles.TripleWord.TripleWord;
import LetterTiles.Blank.Blank;

import info.gridworld.actor.Actor;
import info.gridworld.actor.ActorWorld;
import info.gridworld.grid.BoundedGrid;
import info.gridworld.grid.Grid;
import info.gridworld.grid.Location;

import java.awt.*;
import java.io.File;
import java.io.FileNotFoundException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;


public class ScrabbleRunner {
    public static void main(String[] args) throws FileNotFoundException {
        Scanner scan = new Scanner(System.in);

        // Prints introduction
        printIntro();

        // Init starting conditions
        int numPlayers = getNumPlayers();
        ArrayList<Integer> scores = initScores(numPlayers);
        ArrayList<Actor> tileBag = initTileBag();
        ArrayList<ArrayList<Actor>> playersPieces = initPlayerPieces(numPlayers, tileBag);
        final ArrayList<String> validWords = initValidWords();

        // Creates and shows scrabble board (see ScrabbleBoard Class)
        ActorWorld board = new ScrabbleBoard();
        board.show();


        boolean firstMove = true;  // Special conditions for first move
        int skippedTurns = 0;

        // Continue play until game has ended
        do {
            // For each player in number of players
            for (int i = 0; i < numPlayers; i++) {

                // Check for stalemate game
                if (skippedTurns == numPlayers) {
                    System.out.println("Tile bag is empty and all players have passed, ending game");
                    break;
                }

                System.out.println("\nTiles left in bag: " + tileBag.size());
                System.out.println("\n------------------------");
                System.out.println("Player " + (i + 1) + " turn: ");
                ActorWorld hand = showHand(playersPieces.get(i));  // Shows current player's hand

                // Prompt for new move until move has been made
                boolean playMade = false;
                while (!playMade) {

                    // Get input parameters of play: word, location, direction (See method docs)
                    Object[] playParams = getPlayParams(scan, validWords);

                    // Case for swapping tiles
                    if (playParams == null) {
                        ArrayList<Character> charsSwapped = swapTiles(tileBag, playersPieces.get(i));
                        if (charsSwapped != null) {
                            System.out.println("Letters Swapped: " + charsSwapped);
                            updateHand(hand, playersPieces.get(i));
                        } else {
                            skippedTurns++;
                        }

                        // Prompt to end turn, input not necessarily "end"
                        System.out.println("Close hand and input 'end' to end turn:");
                        scan.next();

                        playMade = true;
                        continue;
                    }

                    String playWord = (String) playParams[0];
                    int startRow = (int) playParams[1];
                    int startCol = (int) playParams[2];
                    char direction = (char) playParams[3];


                    // Get locations to play and raw locations to play, used in calculations (See method docs)
                    ArrayList<Location> locationsPlayedRaw = getLocationsPlayedRaw(startRow, startCol, direction, playWord);
                    ArrayList<Location> locationsPlayed;

                    try {
                        locationsPlayed = getLocationsPlayed(board, startRow, startCol, direction, playWord);
                    } catch (IllegalArgumentException ignore) {
                        // Catch that play is out of board's bounds
                        System.out.println("Play is out of bounds");
                        continue;
                    }

                    // Check that pieces can be placed legally on board
                    if (locationsPlayed == null) {
                        System.out.println("Invalid placement");
                        continue;
                    }

                    // Gets List of letters that must be played, used in calculations
                    ArrayList<Character> lettersPlayed = getLettersPlayed(locationsPlayed, direction, startRow, startCol, playWord, playersPieces.get(i));

                    // Check that there are correct pieces in hand
                    if (lettersPlayed == null) {
                        System.out.println("Cannot be played with current pieces in hand");
                        continue;
                    }
                    if (!isValidPlay(playersPieces.get(i), lettersPlayed)) {
                        System.out.println("Not a valid play");
                        continue;
                    }

                    // Gets list of all words formed, used oin calculations
                    ArrayList<String> wordsFormed = getWordsFormed(board, locationsPlayed, lettersPlayed, playWord, direction, startRow, startCol);

                    // Check that all formed words are in dictionary
                    if (wordsFormed.size() > 1) {
                        String notInDict = "";
                        for (String word : wordsFormed) {
                            if (notInDict(validWords, word))
                                notInDict = word;
                        }
                        if (!notInDict.equals("")) {
                            System.out.println("Additionally formed word [" + notInDict + "] not in dictionary");
                            continue;
                        }
                    }

                    ArrayList<ArrayList<Location>> wordsLocations = getWordsFormedLocations(board, locationsPlayed, lettersPlayed, playWord, direction, startRow, startCol);

                    System.out.println("Words formed: " + wordsFormed);

                    // Checks that played locations intersect existing word
                    if (!firstMove && locationsPlayed.size() == locationsPlayedRaw.size() && wordsFormed.size() < 2) {
                        System.out.println("Played word must intersect existing word");
                        continue;
                    }

                    // Conditional check that first move contains the StartTile
                    if (firstMove && !checkOnStartTile(locationsPlayed)) {
                        System.out.println("Starting word must be on start tile");
                        continue;
                    }


                    int wordScore = 0;

                    // If move is valid, make the move and replenish player's hand if tileBag not empty
                    playOnBoard(board, locationsPlayed, lettersPlayed, playWord, direction, startRow, startCol);
                    ArrayList<Actor> lettersPlayedActors = new ArrayList<>();
                    for (Character c : lettersPlayed) {
                        lettersPlayedActors.add(charToActor(c));
                    }
                    removeLettersFromHand(lettersPlayedActors, playersPieces.get(i));

                    // Checks for Scrabble BINGO (Player earns 50 extra points if they clear all 7 letters from hand)
                    if (playersPieces.get(i).size() == 0) {
                        wordScore = 50;
                        System.out.println("BINGO! +50 points!");
                    }

                    replenishPlayerHand(playersPieces.get(i), tileBag);
                    updateHand(hand, playersPieces.get(i));

                    // Display board updated with move
                    board.show();

                    // Calculate the points gained from the move and adds to current player's score
                    wordScore += calcPoints(wordsLocations, locationsPlayed, board);

                    System.out.println("Points Scored: " + wordScore);
                    scores.set(i, scores.get(i) + wordScore);

                    // Prints total points of each player
                    System.out.println("Total Points: ");
                    for (int j = 0; j < scores.size(); j++) {
                        System.out.println("Player " + (j + 1) + ": " + scores.get(j));
                    }

                    // Prompt to end turn, input not necessarily "end"
                    System.out.println("Close hand and input 'end' to end turn:");
                    scan.next();

                    skippedTurns = 0;
                    firstMove = false;
                    playMade = true;
                }
            }
        } while (!hasEnded(playersPieces) && skippedTurns != numPlayers);

        System.out.println("\nGame End");
        System.out.println("------------------------\n");

        int totalSubScores = 0;
        int emptyHandIdx = -1;

        // Subtracts values of tiles left not played in each player's hand (per Scrabble rules)
        for (int i = 0; i < playersPieces.size(); i++) {
            if (playersPieces.get(i).size() > 0) {
                int endHandScore = calcHandPointsEnd(playersPieces.get(i));
                scores.set(i, scores.get(i) - endHandScore);
                System.out.println("Player " + (i + 1) + " score -" + endHandScore + " for remaining unplaced pieces " + actorsToChars(playersPieces.get(i)));
                totalSubScores += endHandScore;
            } else {
                emptyHandIdx = i;
            }
        }

        // Adds all subtracted scores to empty player's hand, if any (per Scrabble rules)
        if (emptyHandIdx != -1) {
            scores.set(emptyHandIdx, scores.get(emptyHandIdx) + totalSubScores);
            System.out.println("Player " + (emptyHandIdx + 1) + " score +" + totalSubScores + " for other players' remaining peaces");
        }

        // Prints total points of each player at end
        System.out.println("Total Points: ");
        for (int i = 0; i < scores.size(); i++) {
            System.out.println("Player " + (i + 1) + ": " + scores.get(i));
        }
    }


    /**
     * Prints introduction statement
     */
    private static void printIntro() {
        System.out.println("================================================");
        System.out.println("Scrabble Game\n");
        System.out.println("Abridged Rules:");
        System.out.println(" * All played words will automatically be checked to be in dictionary and cannot be challenged");
        System.out.println("\nAll other standard scrabble rules apply");
        System.out.println("\n If play forms multiple words, enter the principle word only. Additional words will be calculated.");
        System.out.println("\nTip: Hover over tile on board to quickly obtain row/col location");
        System.out.println("================================================\n");
    }

    /**
     * Translates a char into the equivalent Actor
     *
     * @param let character of tile
     * @return New Actor representation of character
     */
    public static Actor charToActor(char let) {
        let = Character.toUpperCase(let);
        switch (let) {
            case 'A':
                return new LetterTiles.A.A();
            case 'B':
                return new LetterTiles.B.B();
            case 'C':
                return new LetterTiles.C.C();
            case 'D':
                return new LetterTiles.D.D();
            case 'E':
                return new LetterTiles.E.E();
            case 'F':
                return new LetterTiles.F.F();
            case 'G':
                return new LetterTiles.G.G();
            case 'H':
                return new LetterTiles.H.H();
            case 'I':
                return new LetterTiles.I.I();
            case 'J':
                return new LetterTiles.J.J();
            case 'K':
                return new LetterTiles.K.K();
            case 'L':
                return new LetterTiles.L.L();
            case 'M':
                return new LetterTiles.M.M();
            case 'N':
                return new LetterTiles.N.N();
            case 'O':
                return new LetterTiles.O.O();
            case 'P':
                return new LetterTiles.P.P();
            case 'Q':
                return new LetterTiles.Q.Q();
            case 'R':
                return new LetterTiles.R.R();
            case 'S':
                return new LetterTiles.S.S();
            case 'T':
                return new LetterTiles.T.T();
            case 'U':
                return new LetterTiles.U.U();
            case 'V':
                return new LetterTiles.V.V();
            case 'W':
                return new LetterTiles.W.W();
            case 'X':
                return new LetterTiles.X.X();
            case 'Y':
                return new LetterTiles.Y.Y();
            case 'Z':
                return new LetterTiles.Z.Z();
            case '#':
                return new LetterTiles.Blank.Blank();
        }
        throw new IllegalArgumentException();
    }

    /**
     * Initializer for the tile bag
     *
     * @return shuffled list of Actor tiles
     */
    public static ArrayList<Actor> initTileBag() {
        Actor[] letterArr = new Actor[]{
                new LetterTiles.Blank.Blank(), new LetterTiles.Blank.Blank(),
                new LetterTiles.A.A(), new LetterTiles.A.A(), new LetterTiles.A.A(), new LetterTiles.A.A(),
                new LetterTiles.A.A(), new LetterTiles.A.A(), new LetterTiles.A.A(), new LetterTiles.A.A(),
                new LetterTiles.A.A(), new LetterTiles.B.B(), new LetterTiles.B.B(), new LetterTiles.C.C(),
                new LetterTiles.C.C(), new LetterTiles.D.D(), new LetterTiles.D.D(), new LetterTiles.D.D(),
                new LetterTiles.D.D(), new LetterTiles.E.E(), new LetterTiles.E.E(), new LetterTiles.E.E(),
                new LetterTiles.E.E(), new LetterTiles.E.E(), new LetterTiles.E.E(), new LetterTiles.E.E(),
                new LetterTiles.E.E(), new LetterTiles.E.E(), new LetterTiles.E.E(), new LetterTiles.E.E(),
                new LetterTiles.E.E(), new LetterTiles.F.F(), new LetterTiles.F.F(), new LetterTiles.G.G(),
                new LetterTiles.G.G(), new LetterTiles.G.G(), new LetterTiles.H.H(), new LetterTiles.H.H(),
                new LetterTiles.I.I(), new LetterTiles.I.I(), new LetterTiles.I.I(), new LetterTiles.I.I(),
                new LetterTiles.I.I(), new LetterTiles.I.I(), new LetterTiles.I.I(), new LetterTiles.I.I(),
                new LetterTiles.I.I(), new LetterTiles.J.J(), new LetterTiles.K.K(), new LetterTiles.L.L(),
                new LetterTiles.L.L(), new LetterTiles.L.L(), new LetterTiles.L.L(), new LetterTiles.M.M(),
                new LetterTiles.M.M(), new LetterTiles.N.N(), new LetterTiles.N.N(), new LetterTiles.N.N(),
                new LetterTiles.N.N(), new LetterTiles.N.N(), new LetterTiles.N.N(), new LetterTiles.O.O(),
                new LetterTiles.O.O(), new LetterTiles.O.O(), new LetterTiles.O.O(), new LetterTiles.O.O(),
                new LetterTiles.O.O(), new LetterTiles.O.O(), new LetterTiles.O.O(), new LetterTiles.P.P(),
                new LetterTiles.P.P(), new LetterTiles.Q.Q(), new LetterTiles.R.R(), new LetterTiles.R.R(),
                new LetterTiles.R.R(), new LetterTiles.R.R(), new LetterTiles.R.R(), new LetterTiles.R.R(),
                new LetterTiles.S.S(), new LetterTiles.S.S(), new LetterTiles.S.S(), new LetterTiles.S.S(),
                new LetterTiles.T.T(), new LetterTiles.T.T(), new LetterTiles.T.T(), new LetterTiles.T.T(),
                new LetterTiles.T.T(), new LetterTiles.T.T(), new LetterTiles.U.U(), new LetterTiles.U.U(),
                new LetterTiles.U.U(), new LetterTiles.U.U(), new LetterTiles.V.V(), new LetterTiles.V.V(),
                new LetterTiles.W.W(), new LetterTiles.W.W(), new LetterTiles.X.X(), new LetterTiles.Y.Y(),
                new LetterTiles.Y.Y(), new LetterTiles.Z.Z()
        };
        ArrayList<Actor> letterTileAList = new ArrayList<>(Arrays.asList(letterArr));
        Collections.shuffle(letterTileAList);

        return letterTileAList;
    }

    /**
     * Initializer for an example tile bag
     *
     * @return example tile bag
     */
    private static ArrayList<Actor> initExampleTileBag() {
        Actor[] letterArr = new Actor[]{
                new LetterTiles.J.J(), new LetterTiles.A.A(), new LetterTiles.V.V(), new LetterTiles.A.A(),
                new LetterTiles.P.P(), new LetterTiles.R.R(), new LetterTiles.O.O(),

                new LetterTiles.A.A(), new LetterTiles.L.L(), new LetterTiles.U.U(), new LetterTiles.E.E(),
                new LetterTiles.V.V(), new LetterTiles.A.A(), new LetterTiles.I.I(),

                new LetterTiles.G.G(), new LetterTiles.R.R(), new LetterTiles.M.M(), new LetterTiles.X.X(),

                new LetterTiles.A.A(), new LetterTiles.Blank.Blank(), new LetterTiles.L.L(), new LetterTiles.E.E(),


        };

        return new ArrayList<>(Arrays.asList(letterArr));
    }

    /**
     * Assigns tiles from a tile bag
     * Pieces are assigned from the first 7 indices per player and elements from tileBag removed
     *
     * @param numPlayers number of players 2-4
     * @param tileBag    tile bag to assign pieces from
     * @return a List of a List of Actor tiles
     */
    public static ArrayList<ArrayList<Actor>> initPlayerPieces(int numPlayers, ArrayList<Actor> tileBag) {
        ArrayList<ArrayList<Actor>> playersPieces = new ArrayList<>();
        for (int i = 0; i < numPlayers; i++) {
            ArrayList<Actor> thesePieces = new ArrayList<>();
            for (int j = 0; j < 7; j++) {
                thesePieces.add(tileBag.get(0));
                tileBag.remove(0);
            }
            playersPieces.add(thesePieces);
        }
        return playersPieces;
    }

    /**
     * Initializes a List of valid words from a text file: formatted per line, uppercase
     *
     * @return String List of valid words
     * @throws FileNotFoundException missing reference file of valid words
     */
    public static ArrayList<String> initValidWords() throws FileNotFoundException {
        if (!Files.exists(Path.of("scrabbleWords.txt"))) {
            System.out.println("Scrabble dictionary File 'scrabbleWords.txt' does not exist!");
            System.out.println("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
        }
        File file = new File("scrabbleWords.txt");

        Scanner scan = new Scanner(file);
        ArrayList<String> validWords = new ArrayList<>();
        while (scan.hasNextLine()) {
            validWords.add(scan.nextLine());
        }
        return validWords;
    }

    /**
     * Initializer of scores
     *
     * @param numPlayers number of players 2-4
     * @return List of zeroed scores
     */
    public static ArrayList<Integer> initScores(int numPlayers) {
        ArrayList<Integer> scores = new ArrayList<>();
        for (int i = 0; i < numPlayers; i++) {
            scores.add(0);
        }
        return scores;
    }

    /**
     * Takes user input for number of players 2-4
     *
     * @return number of players
     */
    public static int getNumPlayers() {
        Scanner scan = new Scanner(System.in);
        int numPlayers;

        System.out.println("Number of players 2-4: ");
        numPlayers = scan.nextInt();

        return numPlayers;
    }

    /**
     * Takes input for play parameters
     * playWord: word attempting to be played, or "*" if skipping turn
     * startRow, startCol: coordinates of first letter of word
     * direction: direction that i=word is to be played (h: horizontal, v: vertical)
     *
     * @param scan       Scanner object System.in
     * @param validWords List of valid words
     * @return array of parameters 1: playWord, 2: startRow, 3: startCol, 4: direction; null if player skips turn
     */
    public static Object[] getPlayParams(Scanner scan, ArrayList<String> validWords) {
        Object[] params = new Object[4];

        System.out.println("\nEnter your word ('*' to swap): ");
        String playWord = scan.next().toUpperCase();

        if (playWord.equals("*"))
            return null;

        while (notInDict(validWords, playWord)) {
            System.out.println("Not a valid word");
            System.out.println("\nEnter your word ('*' to swap): ");

            playWord = scan.next().toUpperCase();
            if (playWord.equals("*"))
                return null;
        }

        int startRow, startCol;
        while (true) {
            try {
                System.out.println("Enter starting row:");
                startRow = Integer.parseInt(scan.next());
                System.out.println("Enter starting column:");
                startCol = Integer.parseInt(scan.next());
                break;
            } catch (Exception ignore) {
            }
        }

        char direction;

        do {
            System.out.println("Enter direction (h: horizontal, v: vertical)");
            direction = scan.next().charAt(0);
        } while (direction != 'h' && direction != 'v');

        params[0] = playWord;
        params[1] = startRow;
        params[2] = startCol;
        params[3] = direction;

        return params;
    }

    /**
     * Returns Locations that must be filled to play word, excluding already placed tiles on board
     * -
     * Example:
     * word = "SAMPLE"
     * board contains _A___E
     * returns all blank (_) Locations
     *
     * @param board     ActorWorld of Scrabble board
     * @param startRow  row coordinate of first letter
     * @param startCol  row coordinate of first letter
     * @param direction direction that word is to be played (h: horizontal, v: vertical)
     * @param word      word attempting to be played
     * @return Location List that must be filled to play word, excluding already placed tiles on board
     */
    public static ArrayList<Location> getLocationsPlayed(ActorWorld board, int startRow, int startCol, char direction, String word) {
        Grid<Actor> grid = board.getGrid();

        ArrayList<Location> playerPlayLocations = new ArrayList<>();

        for (int i = 0; i < word.length(); i++) {
            Location boardLoc = new Location(startRow, startCol);
            Actor tileAtLoc = grid.get(boardLoc);
            if (tileNotLetter(tileAtLoc)) {
                playerPlayLocations.add(boardLoc);

            } else if (!(actorToChar(tileAtLoc) == word.charAt(i))) {
                System.out.println("Tile at requested location " + boardLoc + " : " + actorToChar(tileAtLoc));
                System.out.println("Tile necessary: " + word.charAt(i));
                return null;
            }
            if (direction == 'h') {
                startCol++;
            } else if (direction == 'v') {
                startRow++;
            }
        }
        return playerPlayLocations;
    }

    /**
     * Returns Locations that must be filled to play word, including already placed tiles on board
     *
     * @param startRow  row coordinate of first letter
     * @param startCol  row coordinate of first letter
     * @param direction direction that i=word is to be played (h: horizontal, v: vertical)
     * @param word      word attempting to be played
     * @return Location List that must be filled to play word, including already placed tiles on board
     */
    public static ArrayList<Location> getLocationsPlayedRaw(int startRow, int startCol, char direction, String word) {
        ArrayList<Location> playerPlayLocations = new ArrayList<>();

        for (int i = 0; i < word.length(); i++) {
            Location boardLoc = new Location(startRow, startCol);
            playerPlayLocations.add(boardLoc);

            if (direction == 'h') {
                startCol++;
            } else if (direction == 'v') {
                startRow++;
            }
        }
        return playerPlayLocations;
    }

    /**
     * Returns Character List of characters needed to play word
     *
     * @param locationsPlayed Location List that must be filled to play word, excluding already placed tiles on board
     * @param direction       direction that word is to be played (h: horizontal, v: vertical)
     * @param startRow        row coordinate of first letter
     * @param startCol        row coordinate of first letter
     * @param word            word attempting to be played
     * @param playerBoard     Actor List of player's current available tiles
     * @return Character List of characters needed to play word
     */
    public static ArrayList<Character> getLettersPlayed(ArrayList<Location> locationsPlayed, char direction, int startRow, int startCol, String word, ArrayList<Actor> playerBoard) {
        ArrayList<Character> playerPiecesChars = actorsToChars(playerBoard);
        ArrayList<Character> lettersPlayedChars = new ArrayList<>();

        int startIdx = -1;
        if (direction == 'h') {
            startIdx = startCol;
        } else if (direction == 'v') {
            startIdx = startRow;
        }

        int letterIdx;
        for (Location loc : locationsPlayed) {
            char charOfWord = 0;
            if (direction == 'h') {
                letterIdx = loc.getCol() - startIdx;
                charOfWord = word.charAt(letterIdx);
            } else if (direction == 'v') {
                letterIdx = loc.getRow() - startIdx;
                charOfWord = word.charAt(letterIdx);
            }

            if (playerPiecesChars.contains(charOfWord)) {
                playerPiecesChars.remove(Character.valueOf(charOfWord));
                lettersPlayedChars.add(charOfWord);
            } else {
                if (playerPiecesChars.contains('#')) {
                    playerPiecesChars.remove(Character.valueOf('#'));
                    lettersPlayedChars.add('#');
                } else {
                    return null;
                }
            }
        }
        return lettersPlayedChars;
    }

    /**
     * Returns List of all words formed from play
     * -
     * Example: (wordPlayed = "HAT")
     * --HAT
     * THIS-
     * returns [HAT, HI, AS]
     *
     * @param board           ActorWorld Scrabble Board
     * @param locationsPlayed Location List that must be filled to play word, excluding already placed tiles on board
     * @param lettersPlayed   Character List of characters needed to play word
     * @param wordPlayed      original word played
     * @param direction       direction of play (v: vertical, h: horizontal)
     * @param startRow        starting row of word played
     * @param startCol        starting column of word played
     * @return List of all words formed from play
     */
    public static ArrayList<String> getWordsFormed(ActorWorld board, ArrayList<Location> locationsPlayed, ArrayList<Character> lettersPlayed, String wordPlayed, char direction, int startRow, int startCol) {
        ArrayList<String> wordsFormed = new ArrayList<>();

        playOnBoard(board, locationsPlayed, lettersPlayed, wordPlayed, direction, startRow, startCol);
        Grid<Actor> grid = board.getGrid();

        StringBuilder word;

        for (Location loc : locationsPlayed) {
            Location up = loc;
            try {
                while (!tileNotLetter(grid.get(up.getAdjacentLocation(0)))) {
                    up = up.getAdjacentLocation(0);
                }
            } catch (Exception ignore) {
            }

            word = new StringBuilder("" + actorToChar(grid.get(up)));

            try {
                while (!tileNotLetter(grid.get(up.getAdjacentLocation(180)))) {
                    word.append(actorToChar(grid.get(up.getAdjacentLocation(180))));
                    up = up.getAdjacentLocation(180);
                }
            } catch (Exception ignore) {
            }

            if (word.length() > 1) {
                wordsFormed.add(word.toString());
            }
            if (direction == 'v') {
                break;
            }
        }
        for (Location loc : locationsPlayed) {
            Location left = loc;
            try {
                while (!tileNotLetter(grid.get(left.getAdjacentLocation(270)))) {
                    left = left.getAdjacentLocation(270);
                }
            } catch (Exception ignore) {
            }

            word = new StringBuilder("" + actorToChar(grid.get(left)));

            try {
                while (!tileNotLetter(grid.get(left.getAdjacentLocation(90)))) {
                    word.append(actorToChar(grid.get(left.getAdjacentLocation(90))));
                    left = left.getAdjacentLocation(90);
                }
            } catch (Exception ignore) {
            }

            if (word.length() > 1) {
                wordsFormed.add(word.toString());
            }
            if (direction == 'h') {
                break;
            }
        }

        for (Location l : locationsPlayed) {
            ActorWorld example = new ScrabbleBoard();
            Grid<Actor> exGrid = example.getGrid();
            grid.remove(l);
            if (exGrid.get(l) != null) {
                if (exGrid.get(l).getClass().getSimpleName().equals("DoubleLetter")) {
                    grid.put(l, new DoubleLetter());
                } else if (exGrid.get(l).getClass().getSimpleName().equals("TripleLetter")) {
                    grid.put(l, new TripleLetter());
                } else if (exGrid.get(l).getClass().getSimpleName().equals("DoubleWord")) {
                    grid.put(l, new DoubleWord());
                } else if (exGrid.get(l).getClass().getSimpleName().equals("TripleWord")) {
                    grid.put(l, new TripleWord());
                }
            }
        }

        return wordsFormed;
    }

    /**
     * Returns a List of a List of all Locations of each word from play
     * -
     * Example: (wordPlayed = "HAT", top-left = (0, 0))
     * --HAT
     * THIS-
     * returns [[(0, 2), (0, 3), (0, 4)], [(0, 2), (1, 2)], [(0, 3), (1, 3)]
     * for each [HAT, HI, AS]
     *
     * @param board           ActorWorld Scrabble Board
     * @param locationsPlayed Location List that must be filled to play word, excluding already placed tiles on board
     * @param lettersPlayed   Character List of characters needed to play word
     * @param wordPlayed      original word played
     * @param direction       direction of play (v: vertical, h: horizontal)
     * @param startRow        starting row of word played
     * @param startCol        starting column of word played
     * @return List of all words formed from play
     */
    public static ArrayList<ArrayList<Location>> getWordsFormedLocations(ActorWorld board, ArrayList<Location> locationsPlayed, ArrayList<Character> lettersPlayed, String wordPlayed, char direction, int startRow, int startCol) {
        ArrayList<ArrayList<Location>> wordsLocations = new ArrayList<>();

        playOnBoard(board, locationsPlayed, lettersPlayed, wordPlayed, direction, startRow, startCol);
        Grid<Actor> grid = board.getGrid();

        StringBuilder word;
        ArrayList<Location> locsOfWord;

        for (Location loc : locationsPlayed) {
            Location up = loc;

            try {
                while (!tileNotLetter(grid.get(up.getAdjacentLocation(0)))) {
                    up = up.getAdjacentLocation(0);
                }
            } catch (Exception ignore) {
            }

            word = new StringBuilder("" + actorToChar(grid.get(up)));

            locsOfWord = new ArrayList<>();
            locsOfWord.add(up);

            try {
                while (!tileNotLetter(grid.get(up.getAdjacentLocation(180)))) {
                    word.append(actorToChar(grid.get(up.getAdjacentLocation(180))));

                    locsOfWord.add(up.getAdjacentLocation(180));
                    up = up.getAdjacentLocation(180);
                }
            } catch (Exception ignore) {
            }

            if (word.length() > 1) {
                wordsLocations.add(locsOfWord);
            }

            if (direction == 'v') {
                break;
            }
        }

        for (Location loc : locationsPlayed) {
            Location left = loc;
            try {
                while (!tileNotLetter(grid.get(left.getAdjacentLocation(270)))) {
                    left = left.getAdjacentLocation(270);
                }
            } catch (Exception ignore) {
            }

            word = new StringBuilder("" + actorToChar(grid.get(left)));

            locsOfWord = new ArrayList<>();
            locsOfWord.add(left);

            try {
                while (!tileNotLetter(grid.get(left.getAdjacentLocation(90)))) {
                    word.append(actorToChar(grid.get(left.getAdjacentLocation(90))));

                    locsOfWord.add(left.getAdjacentLocation(90));
                    left = left.getAdjacentLocation(90);
                }
            } catch (Exception ignore) {
            }

            if (word.length() > 1) {
                wordsLocations.add(locsOfWord);
            }

            if (direction == 'h') {
                break;
            }
        }


        for (Location l : locationsPlayed) {
            ActorWorld example = new ScrabbleBoard();
            Grid<Actor> exGrid = example.getGrid();
            grid.remove(l);
            if (exGrid.get(l) != null) {
                if (exGrid.get(l).getClass().getSimpleName().equals("DoubleLetter")) {
                    grid.put(l, new DoubleLetter());
                } else if (exGrid.get(l).getClass().getSimpleName().equals("TripleLetter")) {
                    grid.put(l, new TripleLetter());
                } else if (exGrid.get(l).getClass().getSimpleName().equals("DoubleWord")) {
                    grid.put(l, new DoubleWord());
                } else if (exGrid.get(l).getClass().getSimpleName().equals("TripleWord")) {
                    grid.put(l, new TripleWord());
                }
            }
        }

        return wordsLocations;
    }

    /**
     * Checks if word is in a List of valid words
     *
     * @param dict List of valid words
     * @param word word to check
     * @return true if word is NOT in dict, false otherwise
     */
    public static boolean notInDict(ArrayList<String> dict, String word) {
        for (String s : dict) {
            if (s.equals(word))
                return false;
        }
        return true;
    }

    /**
     * Checks if players current available pieces, wild tiles included, can fulfill the required letters
     *
     * @param playerBoard        player's current pieces
     * @param lettersPlayedChars Character List of letters that must be played
     * @return true if player can fulfill the letter requirement, false otherwise
     */
    public static boolean isValidPlay(ArrayList<Actor> playerBoard, ArrayList<Character> lettersPlayedChars) {
        ArrayList<Character> playerPiecesChars = actorsToChars(playerBoard);

        int wildCount = countLetter('#', playerPiecesChars);

        for (Character letter : lettersPlayedChars) {
            if (!playerPiecesChars.remove(letter)) {
                if (wildCount <= 0)
                    return false;
                wildCount--;
            }
        }
        return true;
    }

    /**
     * Takes input for tiles to swap and swaps tiles from the players hand with tiles from the tile bag
     * Replaced letters are inserted and tileBag shuffled before replenishing
     *
     * @param tileBag      Actor List tile bag
     * @param playerPieces Actor List of player's pieces to swap
     * @return Character List of swapped letters
     */
    public static ArrayList<Character> swapTiles(ArrayList<Actor> tileBag, ArrayList<Actor> playerPieces) {
        if (tileBag.size() == 0) {
            System.out.println("Tile bag empty, skipping turn");
            return null;
        }

        Scanner scan = new Scanner(System.in);
        int[] idxArr;

        while (true) {
            try {
                System.out.println("Input indices of tiles to swap, separated by spaces");
                String[] idxArrStr = scan.nextLine().split(" ");
                idxArr = new int[idxArrStr.length];
                for (int i = 0; i < idxArrStr.length; i++) {
                    idxArr[i] = Integer.parseInt(idxArrStr[i]);
                }
                break;
            } catch (Exception ignore) {
            }
        }

        ArrayList<Actor> wordActors = new ArrayList<>();

        for (int i : idxArr) {
            wordActors.add(playerPieces.get(i));
        }

        removeLettersFromHand(wordActors, playerPieces);

        tileBag.addAll(wordActors);
        Collections.shuffle(tileBag);

        replenishPlayerHand(playerPieces, tileBag);

        return actorsToChars(wordActors);
    }


    /**
     * Places tile Actors on board
     * locationsPlayed indices correspond to locations of letters in lettersPlayed
     * <p>
     * Identity of wild tiles adjusted to representative letter, color set to YELLOW to differentiate
     *
     * @param board           ActorWorld Scrabble board
     * @param locationsPlayed locations to be updated
     * @param lettersPlayed   letters to be placed
     * @param word            word to be played (used to determine wild tile identity)
     * @param direction       direction that word is to be played (h: horizontal, v: vertical)
     * @param startRow        starting row of word played
     * @param startCol        starting column of word played
     */
    public static void playOnBoard(ActorWorld board, ArrayList<Location> locationsPlayed, ArrayList<Character> lettersPlayed, String word, char direction, int startRow, int startCol) {
        ArrayList<Actor> lettersPlayedActors = new ArrayList<>();
        for (Character c : lettersPlayed) {
            lettersPlayedActors.add(charToActor(c));
        }

        for (int i = 0; i < locationsPlayed.size(); i++) {
            Actor tile = charToActor(actorToChar(lettersPlayedActors.get(i)));
            Grid<Actor> grid = board.getGrid();
            if (tile instanceof Blank) {
                int letterIdx;
                char charOfWord = 0;
                if (direction == 'h') {
                    letterIdx = locationsPlayed.get(i).getCol() - startCol;
                    charOfWord = word.charAt(letterIdx);
                } else if (direction == 'v') {
                    letterIdx = locationsPlayed.get(i).getRow() - startRow;
                    charOfWord = word.charAt(letterIdx);
                }
                tile = charToActor(charOfWord);
                tile.setColor(new Color(255, 255, 0));
            }
            grid.put(locationsPlayed.get(i), tile);
        }
    }

    /**
     * Removes provided tiles from a player's hand
     *
     * @param wordActors   Actors to remove
     * @param playerPieces Player's Actors to be removed from
     */
    public static void removeLettersFromHand(ArrayList<Actor> wordActors, ArrayList<Actor> playerPieces) {
        ArrayList<Character> wordChars = actorsToChars(wordActors);
        ArrayList<Character> playerChars = actorsToChars(playerPieces);

        for (Character c : wordChars) {
            int idx = playerChars.indexOf(c);
            playerChars.remove(idx);
            playerPieces.remove(idx);
        }
    }

    /**
     * Takes from tileBag to add to player's hand up to 7 pieces
     * No effect after tileBag is empty
     *
     * @param playerPieces Player's hand to replenish
     * @param tileBag      tileBag to take from
     */
    public static void replenishPlayerHand(ArrayList<Actor> playerPieces, ArrayList<Actor> tileBag) {
        while (playerPieces.size() < 7) {
            if (tileBag.size() == 0)
                return;
            playerPieces.add(tileBag.remove(0));
        }
    }

    /**
     * Counts matching letters in a List
     *
     * @param letter      pattern
     * @param letterAList list
     * @return count of matching letters
     */
    public static int countLetter(char letter, ArrayList<Character> letterAList) {
        int letterCount = 0;
        for (Character c : letterAList)
            if (c.equals(letter))
                letterCount++;

        return letterCount;
    }

    /**
     * Returns if an Actor is not a Letter (is Board piece: DoubleLetter, TripleWord, etc.)
     * Used to differentiate board markings from actual Actors
     *
     * @param tile Actor of tile
     * @return true if tile is not a letter Actor, false otherwise
     */
    public static boolean tileNotLetter(Actor tile) {
        return tile == null || tile instanceof DoubleLetter || tile instanceof TripleLetter ||
                tile instanceof DoubleWord || tile instanceof TripleWord || tile instanceof StartTile;
    }

    /**
     * Checks if given locations contain a StartTile
     * Used to fulfill requirement of first placed word
     *
     * @param locationsPlayed Location List played
     * @return true if Location contain a StartTile, false otherwise
     */
    public static boolean checkOnStartTile(ArrayList<Location> locationsPlayed) {
        Grid<Actor> grid = new ScrabbleBoard().getGrid();
        boolean validStart = false;
        for (Location loc : locationsPlayed) {
            if (grid.get(loc) instanceof StartTile)
                validStart = true;
        }

        return validStart;
    }

    /**
     * Returns Character List representation of Actor List
     *
     * @param actorsAList Actor List to translate
     * @return Character List representation
     */
    public static ArrayList<Character> actorsToChars(ArrayList<Actor> actorsAList) {
        ArrayList<Character> pieces = new ArrayList<>();
        for (Actor letterActor : actorsAList) {
            String clsName = letterActor.getClass().getSimpleName();
            if (clsName.equals("Blank")) {
                pieces.add('#');
            } else {
                pieces.add(clsName.charAt(0));
            }
        }
        return pieces;
    }

    /**
     * Returns Character representation of Actor
     *
     * @param actor Actor to translate
     * @return Character representation
     */
    public static char actorToChar(Actor actor) {
        String clsName = actor.getClass().getSimpleName();
        if (clsName.equals("Blank")) {
            return '#';
        } else {
            return clsName.charAt(0);
        }
    }

    /**
     * Updates hand ActorWorld to represent newly drawn pieces in player's hand
     * Separate from showHand() to prevent additional popup
     *
     * @param hand       hand ActorWorld to update
     * @param playerHand player's hand to represent
     */
    public static void updateHand(ActorWorld hand, ArrayList<Actor> playerHand) {
        for (int i = 0; i < playerHand.size(); i++) {
            hand.remove(new Location(0, i));
            hand.add(new Location(0, i), charToActor(actorToChar(playerHand.get(i))));
        }

        for (int i = playerHand.size(); i < 7; i++) {
            hand.remove(new Location(0, i));
        }
        hand.show();
    }

    /**
     * Translates and shows Actor List into ActorWorld of bounded size 1, 7
     *
     * @param playerHand Actor List to translate and show
     * @return ActorWorld representation
     */
    public static ActorWorld showHand(ArrayList<Actor> playerHand) {
        ActorWorld hand = new ActorWorld(new BoundedGrid<>(1, 7));
        for (int i = 0; i < playerHand.size(); i++) {
            hand.add(new Location(0, i), charToActor(actorToChar(playerHand.get(i))));
        }
        hand.show();
        return hand;
    }

    /**
     * Calculates the points scored from a play
     *
     * @param wordsLocations List of a List of the raw locations played for each word
     * @param locationsPlayed List of actual locations played
     * @param board Scrabble board
     * @return points scored
     */
    public static int calcPoints(ArrayList<ArrayList<Location>> wordsLocations, ArrayList<Location> locationsPlayed, ActorWorld board) {
        int scoreTotal = 0;

        for (ArrayList<Location> rawLocs : wordsLocations) {
            int score = 0;

            Grid<Actor> grid = board.getGrid();
            Grid<Actor> gridRaw = new ScrabbleBoard().getGrid();

            for (Location loc : rawLocs) {
                if (grid.get(loc).getColor().getBlue() != 0)
                    score += actorValue(grid.get(loc));
            }

            ArrayList<Location> locationsPlayedForWord = new ArrayList<>(rawLocs);

            for (Location loc : rawLocs) {
                if (!locationsPlayed.contains(loc)) {
                    locationsPlayedForWord.remove(loc);
                }
            }

            int scoreMultiplier = 1;

            for (Location loc : locationsPlayedForWord) {
                if (grid.get(loc).getColor().getBlue() != 0) {
                    if (gridRaw.get(loc) instanceof DoubleLetter || gridRaw.get(loc) instanceof StartTile) {
                        score += actorValue(grid.get(loc));
                    } else if (gridRaw.get(loc) instanceof TripleLetter) {
                        score += 2 * actorValue(grid.get(loc));
                    }
                }
                if (gridRaw.get(loc) instanceof DoubleWord) {
                    scoreMultiplier = 2;
                } else if (gridRaw.get(loc) instanceof TripleWord) {
                    scoreMultiplier = 3;
                }
            }
            scoreTotal += score * scoreMultiplier;
        }
        return scoreTotal;
    }

    /**
     * Calculates total negative value of a player hand
     * Used in determining final score
     *
     * @param playerHand player's hand
     * @return negative value of hand
     */
    public static int calcHandPointsEnd(ArrayList<Actor> playerHand) {
        int score = 0;
        for (Actor letterActor : playerHand) {
            score += actorValue(letterActor);
        }
        return score;
    }

    /**
     * Returns value of a specific tile Actor
     *
     * @param actor Actor to get value of
     * @return value of tile Actor
     */
    public static int actorValue(Actor actor) {
        if (actor.getColor().getBlue() == 0) {
            return 0;
        }
        char letter = actorToChar(actor);

        switch (letter) {
            case 'E':
            case 'A':
            case 'I':
            case 'O':
            case 'N':
            case 'R':
            case 'T':
            case 'L':
            case 'S':
            case 'U':
                return 1;
            case 'D':
            case 'G':
                return 2;
            case 'B':
            case 'C':
            case 'M':
            case 'P':
                return 3;
            case 'F':
            case 'H':
            case 'V':
            case 'W':
            case 'Y':
                return 4;
            case 'K':
                return 5;
            case 'J':
            case 'X':
                return 8;
            case 'Q':
            case 'Z':
                return 10;
        }
        throw new IllegalArgumentException();
    }

    /**
     * Checks if game has ended
     * Conditions: tileBag is empty and a player had played all their pieces
     *
     * @param playersPieces a List of a List of players' pieces
     * @return true if game has ended, false otherwise
     */
    public static boolean hasEnded(ArrayList<ArrayList<Actor>> playersPieces) {
        for (ArrayList<Actor> pieces : playersPieces) {
            if (pieces.size() == 0) {
                return true;
            }
        }
        return false;
    }

}
