import { Box, Paper, Typography } from "@mui/material";

interface Props {
    lyrics: string[];

}

const LyricsPaper = ({ lyrics }: Props) => {
    if (lyrics.length > 0) {
        return (
            <Box
                sx={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    alignItems: 'center',
                    justifyContent: 'center',
                    textAlign: 'center',
                    minWidth: '100%',
                    '& > :not(style)': {
                        m: 1,
                        width: '40%',
                    },
                }}
            >

                <Paper sx={{
                    backgroundColor: "#A9D0F5",
                    padding: '1%',
                }} elevation={3}>
                    {lyrics.map((lyric, index) => (
                        <div key={index}>
                            {lyric.split('\n').map((line, lineIndex) => (
                                <Typography
                                    key={lineIndex}
                                    variant="body1"
                                    sx={{
                                        fontFamily: 'Chilanka, cursive',
                                        fontWeight: 'bold',
                                        fontSize: 16,
                                    }}
                                >
                                    {line}
                                    <br />
                                </Typography>
                            ))}
                            <div style={{ marginBottom: 20 }}></div>
                        </div>
                    ))}
                </Paper>
            </Box >
        )
    }
    return null;
}

export default LyricsPaper;
